import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* ==================================================
           MAIN BACKGROUND
        ================================================== */

        .stApp {
            background: linear-gradient(
                135deg,
                #e8f7ff 0%,
                #f0fff7 50%,
                #e8f8f5 100%
            );

            color: #123b56;
        }


        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }


        /* ==================================================
           SIDEBAR
        ================================================== */

        section[data-testid="stSidebar"] {

            background: linear-gradient(
                180deg,
                #e2f5fc 0%,
                #eafbf5 100%
            );

            border-right: 1px solid #c5e1ea;
        }


        section[data-testid="stSidebar"] * {
            color: #07527a !important;
        }


        /* ==================================================
           SIDEBAR SELECTED PAGE
        ================================================== */

        section[data-testid="stSidebar"] [aria-current="page"] {

            background-color: #d1e6f1 !important;

            border-radius: 7px;
        }


        /* ==================================================
           HEADINGS
        ================================================== */

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


        p {

            color: #285b72;
        }


        /* ==================================================
           LABELS
        ================================================== */

        label {

            color: #145873 !important;

            font-weight: 600 !important;
        }


        /* ==================================================
           NUMBER INPUTS
        ================================================== */

        div[data-baseweb="input"] > div {

            background-color: #dff1f8 !important;

            border: 1px solid #b8dce8 !important;

            border-radius: 8px !important;

            box-shadow: none !important;
        }


        div[data-baseweb="input"] > div:focus-within {

            border: 1px solid #62b6c9 !important;

            box-shadow: 0 0 0 1px #62b6c9 !important;
        }


        input {

            color: #14506b !important;

            background-color: transparent !important;
        }


        /* ==================================================
           SELECT BOX
        ================================================== */

        div[data-baseweb="select"] > div {

            background-color: #dff5ed !important;

            border: 1px solid #b8dfd1 !important;

            border-radius: 8px !important;

            box-shadow: none !important;
        }


        div[data-baseweb="select"] > div:focus-within {

            border: 1px solid #65b99e !important;

            box-shadow: 0 0 0 1px #65b99e !important;
        }


        div[data-baseweb="select"] * {

            color: #145873 !important;
        }


        /* ==================================================
           SELECTBOX DROPDOWN
        ================================================== */

        div[data-baseweb="popover"] {

            background-color: #f0fcf8 !important;
        }


        div[data-baseweb="menu"] {

            background-color: #f0fcf8 !important;
        }


        div[data-baseweb="menu"] * {

            color: #145873 !important;
        }


        /* ==================================================
           SLIDER
        ================================================== */

        div[data-baseweb="slider"] {

            color: #45a88a !important;
        }


        div[data-baseweb="slider"] [role="slider"] {

            background-color: #45a88a !important;

            border-color: #45a88a !important;
        }


        /* ==================================================
           BUTTONS
        ================================================== */

        .stButton > button {

            width: 100%;

            min-height: 45px;

            background: linear-gradient(
                90deg,
                #d6edf7,
                #d8f3e8
            ) !important;

            color: #07527a !important;

            border: 1px solid #acd5df !important;

            border-radius: 9px !important;

            font-weight: 700 !important;

            box-shadow: 0 2px 5px rgba(
                30,
                100,
                120,
                0.08
            );
        }


        .stButton > button:hover {

            background: linear-gradient(
                90deg,
                #c7e8f5,
                #c8eddf
            ) !important;

            color: #064b6d !important;

            border-color: #82c4cf !important;
        }


        .stButton > button:active {

            background-color: #c5e8df !important;
        }


        /* ==================================================
           LINK BUTTON
        ================================================== */

        .stLinkButton > a {

            background: linear-gradient(
                90deg,
                #d6edf7,
                #d8f3e8
            ) !important;

            color: #07527a !important;

            border: 1px solid #acd5df !important;

            border-radius: 9px !important;

            font-weight: 700 !important;
        }


        .stLinkButton > a:hover {

            background: linear-gradient(
                90deg,
                #c7e8f5,
                #c8eddf
            ) !important;

            color: #064b6d !important;
        }


        /* ==================================================
           CONTAINERS / CARDS
        ================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {

            background: rgba(
                255,
                255,
                255,
                0.45
            ) !important;

            border: 1px solid #c5e4e5 !important;

            border-radius: 12px !important;

            box-shadow: 0 2px 8px rgba(
                30,
                100,
                120,
                0.05
            );
        }


        /* ==================================================
           METRICS
        ================================================== */

        [data-testid="stMetric"] {

            background: linear-gradient(
                135deg,
                #e2f4fb,
                #e1f6ed
            ) !important;

            border: 1px solid #c2e0e1 !important;

            border-radius: 12px !important;

            padding: 16px !important;
        }


        [data-testid="stMetricLabel"] {

            color: #377083 !important;
        }


        [data-testid="stMetricValue"] {

            color: #07527a !important;

            font-weight: 800 !important;
        }


        /* ==================================================
           EXPANDER
        ================================================== */

        div[data-testid="stExpander"] {

            background-color: rgba(
                239,
                251,
                247,
                0.8
            ) !important;

            border: 1px solid #c5e1dc !important;

            border-radius: 10px !important;
        }


        div[data-testid="stExpander"] * {

            color: #145873;
        }


        /* ==================================================
           SUCCESS MESSAGE
        ================================================== */

        div[data-testid="stAlert"] {

            border-radius: 10px !important;
        }


        /* ==================================================
           DIVIDER
        ================================================== */

        hr {

            border-color: #c5e0e3 !important;
        }


        /* ==================================================
           DATAFRAME
        ================================================== */

        [data-testid="stDataFrame"] {

            border: 1px solid #c5e0e3;

            border-radius: 8px;
        }


        /* ==================================================
           CHAT MESSAGE
        ================================================== */

        div[data-testid="stChatMessage"] {

            background-color: rgba(
                225,
                246,
                241,
                0.75
            ) !important;

            border: 1px solid #c6e3df !important;

            border-radius: 12px !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )