
from pathlib import Path
from datetime import datetime
import pickle
import shutil
import re

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ==========================================================
# 1. PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = BASE_DIR / "documents"
VECTOR_DB_PATH = BASE_DIR / "vector_db"

CHUNKS_PATH = BASE_DIR / "rag" / "chunks.pkl"
RESTRICTED_PATH = BASE_DIR / "rag" / "restricted_chunks.pkl"
REVIEW_PATH = BASE_DIR / "rag" / "review_chunks.pkl"


# ==========================================================
# 2. CHUNK SETTINGS
# ==========================================================

CHUNK_SIZE = 350
CHUNK_OVERLAP = 40


# ==========================================================
# 3. RESTRICTED KEYWORDS
# ==========================================================

RESTRICTED_KEYWORDS = [
    "normalized decision matrix",
    "weighted normalized decision matrix",
    "normalized torque",
    "normalized power",
    "predicted torque",
    "predicted power",
    "raw experimental data",
    "internal research data",
    "research dataset",
    "topsis score",
    "topsis ranking",
    "positive ideal solution (pis)",
    "negative ideal solution (nis)",
]


# ==========================================================
# 4. REGULAR EXPRESSIONS
# ==========================================================

NUMBER_PATTERN = r"\b\d+(?:\.\d+)?\b"

# TOPSIS rows: RPM followed by normalized values.
TOPSIS_ROW_PATTERN = re.compile(
    r"^\s*\d{3,5}\s+0\.\d+",
    re.MULTILINE
)

# ARAI corrosion rows: material ID and decimal measurements.
ARAI_ROW_PATTERN = re.compile(
    r"^\s*\d+\s+M\d+\s+\([^)]*\)\s+[-+]?\d+\.\d+",
    re.MULTILINE
)

# Numbered bibliography references:
# 22. Author
# [22] Author
# 22) Author
REFERENCE_NUMBER_PATTERN = re.compile(
    r"^\s*(?:\[\d{1,3}\]|\d{1,3}[.)])\s+\S",
    re.MULTILINE
)


# ==========================================================
# 5. BASIC HELPER FUNCTIONS
# ==========================================================

def has_numeric_data(text):
    numbers = re.findall(NUMBER_PATTERN, text)
    return len(numbers) >= 3


def contains_numeric_table(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if len(lines) < 3:
        return False

    numeric_lines = 0

    for line in lines:

        numbers = re.findall(
            NUMBER_PATTERN,
            line
        )

        if len(numbers) >= 3:
            numeric_lines += 1

    ratio = numeric_lines / len(lines)

    return (
        numeric_lines >= 3
        and ratio >= 0.40
    )


# ==========================================================
# 6. KNOWN RESTRICTED TABLE DETECTION
# ==========================================================

def is_known_restricted_table(text, source, page):

    filename = Path(source).name.lower()
    page = str(page)

    # A. TOPSIS numerical tables

    if (
        filename == "588602204.pdf"
        and page == "8"
        and contains_numeric_table(text)
        and TOPSIS_ROW_PATTERN.search(text)
    ):
        return True

    # B. ARAI corrosion measurements

    if (
        filename == "arai journal e20.pdf"
        and page == "3"
        and ARAI_ROW_PATTERN.search(text)
    ):
        return True

    # C. Experimental test-fuel properties

    if (
        filename == "588602204.pdf"
        and page == "2"
        and "table 1 properties of test fuels" in text.lower()
    ):
        return True

    return False


# ==========================================================
# 7. EXPERIMENTAL NUMERICAL RESULTS
# ==========================================================

def is_experimental_numerical_result(text, source, page):

    lower = text.lower()

    filename = Path(source).name.lower()
    page = str(page)

    # Known quantitative torque finding from the audit.

    if (
        filename == "11.+45419.pdf"
        and page == "4"
        and "torque" in lower
        and has_numeric_data(text)
    ):
        return True

    experimental_terms = [
        "experimental",
        "experimentally",
        "experimental investigation",
        "experimental study",
        "test results",
    ]

    quantitative_terms = [
        "%",
        "increased by",
        "decreased by",
        "reduction of",
        "increment",
        "improvement",
        "emission",
        "torque",
        "power",
        "bsfc",
    ]

    has_experimental_context = any(
        term in lower
        for term in experimental_terms
    )

    has_quantitative_context = (
        has_numeric_data(text)
        and any(
            term in lower
            for term in quantitative_terms
        )
    )

    return (
        has_experimental_context
        and has_quantitative_context
    )


# ==========================================================
# 8. PUBLIC BIBLIOGRAPHY DETECTION
# ==========================================================

def is_bibliography(text):
    lower = text.lower()

    bibliography_indicators = [
        "doi.org/",
        "doi:",
        "references",
        "renew energy",
        "applied energy",
        "energy conversion and management",
        "mater today",
        "technical paper",
        "proceedings",
        "journal",
        "vol.",
        "pp.",
    ]

    has_reference_number = bool(
        REFERENCE_NUMBER_PATTERN.search(text)
    )

    has_bibliography_indicator = any(
        term in lower for term in bibliography_indicators
    )

    has_doi = "doi.org/" in lower or "doi:" in lower

    return (
        has_bibliography_indicator
        and (has_reference_number or has_doi)
    )

# ==========================================================
# 9. PUBLIC FUEL-PROPERTY TABLE DETECTION
# ==========================================================

def is_public_fuel_property_table(text):

    lower = text.lower()

    property_terms = [
        "density",
        "boiling point",
        "heat of vaporization",
        "chemical formula",
        "calorific value",
        "auto-ignition temperature",
        "oxygen (% wt.)",
        "stoichiometric afr",
        "flammable limits",
        "latent heating value",
    ]

    matched_terms = sum(
        term in lower
        for term in property_terms
    )

    return matched_terms >= 3


# ==========================================================
# 10. PUBLIC ETHANOL POLICY DETECTION
# ==========================================================

def is_public_ethanol_policy(text, source):

    lower = text.lower()
    source_lower = Path(source).name.lower()

    policy_document = (
        "ethanolblendinginindia" in source_lower
    )

    policy_terms = [
        "ethanol supply",
        "ethanol blending",
        "quantity supplied",
        "crore litres",
        "blending percentage",
        "blending target",
        "ethanol production capacity",
    ]

    has_policy_terms = any(
        term in lower
        for term in policy_terms
    )

    return (
        policy_document
        or has_policy_terms
    )


# ==========================================================
# 11. PUBLIC VEHICLE COMPATIBILITY INFORMATION
# ==========================================================

def is_public_compatibility_information(text):

    lower = text.lower()

    compatibility_terms = [
        "e20 compatible",
        "e20 compatibility",
        "compatible with e20",
        "e20 fuel",
        "warranty",
        "volkswagen",
    ]

    has_compatibility_term = any(
        term in lower
        for term in compatibility_terms
    )

    has_vehicle_context = any(
        term in lower
        for term in [
            "vehicle",
            "engine",
            "fuel",
            "e20",
        ]
    )

    return (
        has_compatibility_term
        and has_vehicle_context
    )


# ==========================================================
# 12. CLASSIFICATION FUNCTION
# ==========================================================

def classify_chunk(text, source, page):

    lower = text.lower()

    # RULE 1: Known restricted numerical tables

    if is_known_restricted_table(
        text,
        source,
        page
    ):
        return (
            "restricted",
            "research_numerical_table"
        )

    # RULE 2: Explicit restricted keywords

    if any(
        keyword in lower
        for keyword in RESTRICTED_KEYWORDS
    ):
        return (
            "restricted",
            "research_data"
        )

    # RULE 3: Quantitative experimental results

    if is_experimental_numerical_result(
        text,
        source,
        page
    ):
        return (
            "restricted",
            "experimental_numerical_result"
        )

    # RULE 4: Public bibliography

    if is_bibliography(text):
        return (
            "public",
            "bibliography"
        )

    # RULE 5: Public ethanol policy statistics

    if is_public_ethanol_policy(
        text,
        source
    ):
        return (
            "public",
            "ethanol_policy_information"
        )

    # RULE 6: Public E20 compatibility and warranty

    if is_public_compatibility_information(text):
        return (
            "public",
            "vehicle_compatibility_information"
        )

    # RULE 7: Public general fuel properties

    if is_public_fuel_property_table(text):
        return (
            "public",
            "fuel_properties"
        )

    # RULE 8: Uncertain numerical tables

    if contains_numeric_table(text):
        return (
            "review_required",
            "possible_numeric_table"
        )

    # RULE 9: General explanations

    return (
        "public",
        "general_information"
    )


# ==========================================================
# 13. LOAD PDF DOCUMENTS
# ==========================================================

print("\nLoading PDF documents...")

if not DOCUMENTS_PATH.exists():

    raise FileNotFoundError(
        f"Documents folder not found: {DOCUMENTS_PATH}"
    )

loader = PyPDFDirectoryLoader(
    str(DOCUMENTS_PATH)
)

documents = loader.load()

print(
    f"Total PDF pages loaded: {len(documents)}"
)


# ==========================================================
# 14. SPLIT DOCUMENTS INTO CHUNKS
# ==========================================================

print("\nSplitting documents into chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

chunks = text_splitter.split_documents(
    documents
)

print(
    f"Total chunks created: {len(chunks)}"
)


# ==========================================================
# 15. CLASSIFY CHUNKS
# ==========================================================

public_chunks = []
restricted_chunks = []
review_chunks = []

print("\nClassifying chunks...")

for chunk in chunks:

    source = str(
        chunk.metadata.get("source", "")
    )

    page = chunk.metadata.get(
        "page",
        ""
    )

    access_level, content_type = classify_chunk(
        chunk.page_content,
        source,
        page
    )

    chunk.metadata["access_level"] = access_level
    chunk.metadata["content_type"] = content_type

    if access_level == "public":

        public_chunks.append(chunk)

    elif access_level == "restricted":

        restricted_chunks.append(chunk)

    else:

        review_chunks.append(chunk)


# ==========================================================
# 16. SAVE CLASSIFIED CHUNKS
# ==========================================================

print("\nSaving classified chunks...")

CHUNKS_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(CHUNKS_PATH, "wb") as file:

    pickle.dump(
        public_chunks,
        file
    )

with open(RESTRICTED_PATH, "wb") as file:

    pickle.dump(
        restricted_chunks,
        file
    )

with open(REVIEW_PATH, "wb") as file:

    pickle.dump(
        review_chunks,
        file
    )

print("Classified chunks saved.")


# ==========================================================
# 17. BACKUP EXISTING VECTOR DATABASE
# ==========================================================

if VECTOR_DB_PATH.exists():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_path = BASE_DIR / (
        f"vector_db_backup_{timestamp}"
    )

    print(
        "\nBacking up existing vector database..."
    )

    shutil.copytree(
        VECTOR_DB_PATH,
        backup_path
    )

    print(
        f"Backup created: {backup_path}"
    )


# ==========================================================
# 18. CREATE PUBLIC-ONLY VECTOR DATABASE
# ==========================================================

print("\nCreating public-only vector database...")

if not public_chunks:

    raise ValueError(
        "No public chunks found. "
        "Vector database was not rebuilt."
    )

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

if VECTOR_DB_PATH.exists():

    shutil.rmtree(
        VECTOR_DB_PATH
    )

vector_db = Chroma.from_documents(
    documents=public_chunks,
    embedding=embeddings,
    persist_directory=str(VECTOR_DB_PATH)
)

print(
    "Public ChromaDB created successfully."
)


# ==========================================================
# 19. SAVE PUBLIC CHUNKS FOR BM25
# ==========================================================

with open(CHUNKS_PATH, "wb") as file:

    pickle.dump(
        public_chunks,
        file
    )

print(
    "Public BM25 chunks saved successfully."
)


# ==========================================================
# 20. FINAL INDEXING REPORT
# ==========================================================

print("\n" + "=" * 55)
print("INDEXING COMPLETED")
print("=" * 55)

print(
    f"Total chunks       : {len(chunks)}"
)

print(
    f"Public chunks      : {len(public_chunks)}"
)

print(
    f"Restricted chunks  : {len(restricted_chunks)}"
)

print(
    f"Review required    : {len(review_chunks)}"
)


# ==========================================================
# 21. CLASSIFICATION BREAKDOWN
# ==========================================================

for label, items in [
    ("PUBLIC", public_chunks),
    ("RESTRICTED", restricted_chunks),
    ("REVIEW_REQUIRED", review_chunks),
]:

    print(f"\n{label}:")

    counts = {}

    for item in items:

        content_type = item.metadata.get(
            "content_type",
            "unknown"
        )

        counts[content_type] = (
            counts.get(content_type, 0) + 1
        )

    for content_type, count in counts.items():

        print(
            f"  {content_type}: {count}"
        )


# ==========================================================
# 22. FINAL STATUS
# ==========================================================

print("\nStorage:")

print("ChromaDB          : Public chunks only")
print("BM25              : Public chunks only")
print("Restricted data   : Separate pickle file")
print("Review data       : Separate pickle file")

print("\nIMPORTANT:")

print("Restricted chunks are NOT indexed.")
print("Review chunks are NOT indexed.")
print("Only public chunks are available to RAG.")

print("\nINDEXING FINISHED")
