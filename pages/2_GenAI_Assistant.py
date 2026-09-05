import streamlit as st

from style import apply_theme
from rag.rag_chain import ask_rag
from rag.memory import clear_history


st.set_page_config(
    page_title="GenAI Vehicle Assistant",
    page_icon="🤖",
    layout="wide",
)

apply_theme()


# =========================================================
# HEADER
# =========================================================

st.title("🤖 GenAI Vehicle Assistant")

st.write(
    "Ask questions about ethanol fuel, mileage, engine performance "
    "and vehicle behavior."
)

st.caption(
    "🔎 Hybrid RAG Search  •  📚 Vehicle Knowledge Base  •  ⚡ Groq LLM"
)

st.divider()


# =========================================================
# FEATURE CARDS
# =========================================================

st.subheader("🧠 AI Capabilities")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("### 🔎 Hybrid RAG")
        st.write(
            "Combines vector search and BM25 keyword search "
            "to retrieve relevant information."
        )

with c2:
    with st.container(border=True):
        st.markdown("### 📚 Knowledge Base")
        st.write(
            "Uses project documents and vehicle dataset information "
            "to ground responses."
        )

with c3:
    with st.container(border=True):
        st.markdown("### ⚡ Groq LLM")
        st.write(
            "Generates fast, grounded answers using the retrieved context."
        )


st.divider()


# =========================================================
# CHAT
# =========================================================

st.subheader("💬 Ask Your Question")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input(
    "Ask anything about vehicles, mileage or ethanol blends..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("🔎 Searching knowledge base..."):

            try:
                answer = ask_rag(question)

            except Exception as e:
                answer = (
                    "⚠️ Unable to generate a response.\n\n"
                    f"Error: `{e}`"
                )

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🤖 GenAI Assistant")

st.sidebar.success("Hybrid Search Enabled")

st.sidebar.markdown("---")

st.sidebar.write("✔ Chroma Vector Search")
st.sidebar.write("✔ BM25 Keyword Search")
st.sidebar.write("✔ Vehicle Dataset Search")
st.sidebar.write("✔ Conversation Memory")
st.sidebar.write("✔ Source References")
st.sidebar.write("✔ Groq LLM")

st.sidebar.markdown("---")

if st.sidebar.button(
    "🗑 Clear Chat",
    use_container_width=True,
):

    st.session_state.messages = []

    clear_history()

    st.rerun()


st.divider()

st.info(
    "💡 Tip: Ask questions such as "
    "'What factors affect vehicle mileage?' or "
    "'What is the average mileage of Honda City?'"
)

st.caption(
    "⚠️ Responses are generated from available project knowledge "
    "and may not always be 100% accurate."
)