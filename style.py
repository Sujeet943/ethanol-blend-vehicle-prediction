import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>

        /* =========================================================
           MAIN APP
        ========================================================= */

        .stApp {
            background: linear-gradient(
                135deg,
                #e8f7ff 0%,
                #f4fff9 50%,
                #e8f8f5 100%
            ) !important;

            color: #164f68 !important;
        }

        .main {
            background: transparent !important;
        }

        .block-container {
            max-width: 1200px !important;
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
        }


        /* =========================================================
           SIDEBAR
           ========================================================= */

        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #e3f5fc 0%,
                #eafbf5 100%
            ) !important;

            border-right: 1px solid #c5e2e8 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #07527a !important;
        }

        section[data-testid="stSidebar"] a {
            color: #07527a !important;
        }

        section[data-testid="stSidebar"] a:hover {
            background-color: #d5edf4 !important;
        }


        /* =========================================================
           HEADINGS
           ========================================================= */

        h1 {
            color: #07527a !important;
            font-weight: 800 !important;
        }

        h2 {
            color: #086080 !important;
            font-weight: 750 !important;
        }

        h3 {
            color: #08705f !important;
            font-weight: 700 !important;
        }


        /* =========================================================
           NORMAL TEXT
           ========================================================= */

        p {
            color: #285b72 !important;
        }

        .stMarkdown {
            color: #285b72 !important;
        }

        .stMarkdown p {
            color: #285b72 !important;
        }


        /* =========================================================
           MARKDOWN BULLET POINTS
           FIXES WHITE TEXT IN RAG / GENAI ANSWERS
           ========================================================= */

        .stMarkdown li {
            color: #285b72 !important;
        }

        .stMarkdown li p {
            color: #285b72 !important;
        }

        .stMarkdown ul {
            color: #285b72 !important;
        }

        .stMarkdown ol {
            color: #285b72 !important;
        }

        .stMarkdown li::marker {
            color: #285b72 !important;
        }


        /* =========================================================
           CHAT MESSAGE TEXT
           ========================================================= */

        div[data-testid="stChatMessage"] {
            background-color: rgba(
                225,
                246,
                241,
                0.8
            ) !important;

            border: 1px solid #c5e2de !important;
            border-radius: 12px !important;
        }

        div[data-testid="stChatMessage"] p {
            color: #285b72 !important;
        }

        div[data-testid="stChatMessage"] li {
            color: #285b72 !important;
        }

        div[data-testid="stChatMessage"] li p {
            color: #285b72 !important;
        }

        div[data-testid="stChatMessage"] ul {
            color: #285b72 !important;
        }

        div[data-testid="stChatMessage"] ol {
            color: #285b72 !important;
        }

        div[data-testid="stChatMessage"] li::marker {
            color: #285b72 !important;
        }

        div[data-testid="stChatMessage"] h1 {
            color: #07527a !important;
        }

        div[data-testid="stChatMessage"] h2 {
            color: #086080 !important;
        }

        div[data-testid="stChatMessage"] h3 {
            color: #08705f !important;
        }


        /* =========================================================
           WIDGET LABELS
           ========================================================= */

        label {
            color: #145873 !important;
            font-weight: 600 !important;
        }

        [data-testid="stWidgetLabel"] {
            color: #145873 !important;
        }

        [data-testid="stWidgetLabel"] p {
            color: #145873 !important;
        }


        /* =========================================================
           NUMBER INPUT
           ========================================================= */

        div[data-testid="stNumberInput"] {
            background: transparent !important;
        }

        div[data-testid="stNumberInput"]
        div[data-baseweb="input"] {
            background-color: #dff2f8 !important;
            border: 1px solid #9fcbd9 !important;
            border-radius: 9px !important;
        }

        div[data-testid="stNumberInput"]
        div[data-baseweb="input"] > div {
            background-color: #dff2f8 !important;
            border: none !important;
        }

        div[data-testid="stNumberInput"] input {
            background-color: #dff2f8 !important;
            color: #164f68 !important;
            -webkit-text-fill-color: #164f68 !important;
        }

        div[data-testid="stNumberInput"] button {
            background-color: #dff2f8 !important;
            color: #07527a !important;
            border: none !important;
        }

        div[data-testid="stNumberInput"] button:hover {
            background-color: #c9e9f2 !important;
        }


        /* =========================================================
           SELECT BOX
           ========================================================= */

        div[data-testid="stSelectbox"] {
            background: transparent !important;
        }

        div[data-testid="stSelectbox"]
        div[data-baseweb="select"] {
            background-color: #dff5ed !important;
        }

        div[data-testid="stSelectbox"]
        div[data-baseweb="select"] > div {
            background-color: #dff5ed !important;
            border: 1px solid #a7d6c5 !important;
            border-radius: 9px !important;
        }

        div[data-testid="stSelectbox"]
        div[data-baseweb="select"] * {
            color: #145873 !important;
        }

        div[data-testid="stSelectbox"] svg {
            fill: #08705f !important;
        }


        /* =========================================================
           SELECTBOX DROPDOWN
           ========================================================= */

        div[data-baseweb="popover"] {
            background-color: #f0fcf8 !important;
        }

        div[data-baseweb="menu"] {
            background-color: #f0fcf8 !important;
        }

        div[data-baseweb="menu"] li {
            color: #145873 !important;
        }

        div[data-baseweb="menu"] li:hover {
            background-color: #d9f1e8 !important;
        }


        /* =========================================================
           SLIDER
           ========================================================= */

        div[data-testid="stSlider"] {
            color: #42a889 !important;
        }

        div[data-testid="stSlider"] [role="slider"] {
            background-color: #42a889 !important;
            border-color: #42a889 !important;
        }


        /* =========================================================
           BUTTONS
           ========================================================= */

        div.stButton > button {
            background: linear-gradient(
                90deg,
                #d6edf7,
                #d8f3e8
            ) !important;

            color: #07527a !important;
            border: 1px solid #a6d4df !important;
            border-radius: 9px !important;
            min-height: 45px !important;
            font-weight: 700 !important;
        }

        div.stButton > button p {
            color: #07527a !important;
            font-weight: 700 !important;
        }

        div.stButton > button:hover {
            background: linear-gradient(
                90deg,
                #c5e7f4,
                #c6eddf
            ) !important;

            border-color: #7dbdca !important;
        }


        /* =========================================================
           LINK BUTTON
           ========================================================= */

        .stLinkButton > a {
            background: linear-gradient(
                90deg,
                #d6edf7,
                #d8f3e8
            ) !important;

            color: #07527a !important;
            border: 1px solid #a6d4df !important;
            border-radius: 9px !important;
            font-weight: 700 !important;
        }

        .stLinkButton > a:hover {
            background: linear-gradient(
                90deg,
                #c5e7f4,
                #c6eddf
            ) !important;
        }


        /* =========================================================
           CONTAINERS / CARDS
           ========================================================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(
                255,
                255,
                255,
                0.45
            ) !important;

            border: 1px solid #c4e1e2 !important;
            border-radius: 12px !important;

            box-shadow: 0 2px 8px rgba(
                30,
                100,
                120,
                0.05
            ) !important;
        }


        /* =========================================================
           METRIC
           ========================================================= */

        [data-testid="stMetric"] {
            background: linear-gradient(
                135deg,
                #e0f3fa,
                #e0f5eb
            ) !important;

            border: 1px solid #c1dedf !important;
            border-radius: 12px !important;
            padding: 18px !important;
        }

        [data-testid="stMetricLabel"] {
            color: #377083 !important;
        }

        [data-testid="stMetricValue"] {
            color: #07527a !important;
            font-weight: 800 !important;
        }


        /* =========================================================
           EXPANDER
           ========================================================= */

        div[data-testid="stExpander"] {
            background-color: #eefaf7 !important;
            border: 1px solid #c4e0db !important;
            border-radius: 10px !important;
        }

        div[data-testid="stExpander"] summary {
            color: #07527a !important;
        }

        div[data-testid="stExpander"] summary p {
            color: #07527a !important;
            font-weight: 600 !important;
        }


        /* =========================================================
           ALERTS
           ========================================================= */

        div[data-testid="stAlert"] {
            border-radius: 10px !important;
        }


        /* =========================================================
           DIVIDERS
           ========================================================= */

        hr {
            border-color: #c5e0e3 !important;
        }


        /* =========================================================
           DATAFRAME
           ========================================================= */

        div[data-testid="stDataFrame"] {
            border: 1px solid #c5e0e3 !important;
            border-radius: 8px !important;
        }


        </style>
        """,
        unsafe_allow_html=True
    )