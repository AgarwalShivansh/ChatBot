import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)
import textwrap
import html


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Mood Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>


@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* =====================================================
   GLOBAL
===================================================== */

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(255, 115, 0, 0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(255, 140, 40, 0.06),
            transparent 30%
        ),
        #080808;

    color: #f5f5f5;
}


/* =====================================================
   HIDE STREAMLIT DEFAULT UI
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* =====================================================
   MAIN CONTAINER
===================================================== */

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* =====================================================
   LEFT SIDE TITLE
===================================================== */

.app-title {
    font-size: 2.3rem;
    font-weight: 700;
    color: #f2f2f2;
    margin-bottom: 0.4rem;
    animation: fadeDown 0.7s ease;
}

.app-title span {
    background: linear-gradient(
        90deg,
        #ff6a00,
        #ff8c1a,
        #ffb15c
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.app-subtitle {
    color: #969696;
    font-size: 1rem;
    margin-bottom: 2.5rem;
}


/* =====================================================
   MODE SECTION
===================================================== */

.mode-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #ff8a1f;
    margin-bottom: 0.8rem;
}


/* =====================================================
   RADIO BUTTONS
===================================================== */

.stRadio {
    margin-bottom: 1rem;
}

.stRadio label {
    color: #d6d6d6 !important;
    font-size: 0.95rem !important;
}


/* =====================================================
   MODE CARDS
===================================================== */

.mode-card {
    border: 1px solid #2c2c2c;
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 0.8rem;

    background: linear-gradient(
        135deg,
        #1b1b1b,
        #111111
    );

    transition:
        transform 0.3s ease,
        border 0.3s ease,
        box-shadow 0.3s ease;

    animation: cardAppear 0.5s ease;
}

.mode-card:hover {
    transform: translateY(-4px);

    border-color: rgba(255, 115, 0, 0.75);

    box-shadow:
        0 12px 35px rgba(255, 98, 0, 0.12);
}


/* Active mode */

.active-mode {
    border-color: #ff7300;

    box-shadow:
        0 0 22px rgba(255, 115, 0, 0.14);
}


.mode-title {
    color: #f2f2f2;
    font-weight: 600;
    font-size: 1rem;
}

.mode-description {
    color: #969696;
    font-size: 0.82rem;
    margin-top: 0.4rem;
}


/* =====================================================
   CHAT HEADER
===================================================== */

.chat-header {
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.5rem;

    border-radius: 20px;

    border: 1px solid #2b2b2b;

    background: linear-gradient(
        135deg,
        #1a1a1a,
        #101010
    );

    animation: fadeDown 0.7s ease;
}

.chat-title {
    font-size: 1.7rem;
    font-weight: 700;
    color: #f5f5f5;
}

.chat-title span {
    background: linear-gradient(
        90deg,
        #ff6500,
        #ff8c1a,
        #ffb35c
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.chat-subtitle {
    margin-top: 0.35rem;
    color: #8d8d8d;
    font-size: 0.9rem;
}


/* =====================================================
   USER MESSAGE - RIGHT
===================================================== */

.user-message {
    display: flex;
    justify-content: flex-end;
    width: 100%;
    margin: 14px 0;

    animation: slideRight 0.4s ease;
}

.user-bubble {
    max-width: 68%;

    padding: 13px 18px;

    border-radius:
        22px 22px 5px 22px;

    background: linear-gradient(
        135deg,
        #ff5e00,
        #ff7a00,
        #ff9d32
    );

    color: #ffffff;

    font-size: 0.95rem;

    line-height: 1.5;

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 8px 28px rgba(255, 94, 0, 0.20);
}


/* =====================================================
   AI MESSAGE - LEFT
===================================================== */

.ai-message {
    display: flex;
    justify-content: flex-start;
    width: 100%;
    margin: 14px 0;

    animation: slideLeft 0.4s ease;
}

.ai-bubble {
    max-width: 68%;

    padding: 13px 18px;

    border-radius:
        22px 22px 22px 5px;

    background: linear-gradient(
        135deg,
        #2a2a2a,
        #1b1b1b
    );

    color: #e7e7e7;

    font-size: 0.95rem;

    line-height: 1.6;

    border: 1px solid #3a3a3a;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.25);
}


/* =====================================================
   PREMIUM CHAT INPUT
===================================================== */

[data-testid="stChatInput"] {

    background: linear-gradient(
        135deg,
        #242424,
        #171717
    ) !important;

    border: 1px solid #353535 !important;

    border-radius: 18px !important;

    padding: 7px 10px !important;

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.35);

    transition:
        border 0.3s ease,
        box-shadow 0.3s ease,
        transform 0.3s ease;
}


/* Orange glow while typing */

[data-testid="stChatInput"]:focus-within {

    border-color:
        rgba(255, 115, 0, 0.85) !important;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.45),
        0 0 22px rgba(255, 102, 0, 0.16);

    transform: translateY(-2px);
}


/* Input text */

[data-testid="stChatInput"] textarea {

    background: transparent !important;

    color: #f5f5f5 !important;

    font-size: 0.95rem !important;

    padding: 8px 12px !important;

    min-height: 35px !important;

    caret-color: #ff7300 !important;
}


/* Placeholder */

[data-testid="stChatInput"] textarea::placeholder {

    color: #777777 !important;

    opacity: 1 !important;
}


/* Send button */

[data-testid="stChatInput"] button {

    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;

    border-radius: 50% !important;

    border: none !important;

    background: linear-gradient(
        135deg,
        #ff5500,
        #ff7a00,
        #ff9d32
    ) !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


/* Send button hover */

[data-testid="stChatInput"] button:hover {

    transform: scale(1.08) rotate(-6deg) !important;

    box-shadow:
        0 5px 22px rgba(255, 100, 0, 0.45);
}


[data-testid="stChatInput"] button:active {
    transform: scale(0.92) !important;
}


/* Arrow size */

[data-testid="stChatInput"] button svg {
    width: 17px !important;
    height: 17px !important;
}


/* =====================================================
   CLEAR CHAT BUTTON
===================================================== */

.stButton > button {

    width: 100%;

    border: 1px solid #3a3a3a;

    border-radius: 14px;

    padding: 0.6rem;

    background: linear-gradient(
        135deg,
        #242424,
        #171717
    );

    color: #e8e8e8;

    font-weight: 600;

    transition: all 0.3s ease;
}


.stButton > button:hover {

    border-color: #ff7300;

    color: #ffffff;

    transform: translateY(-3px);

    box-shadow:
        0 10px 25px rgba(255, 100, 0, 0.16);
}


/* =====================================================
   GLOW ORB
===================================================== */

.orb {

    width: 120px;
    height: 120px;

    border-radius: 50%;

    margin: 3rem auto;

    background: radial-gradient(
        circle,
        rgba(255, 106, 0, 0.35),
        rgba(255, 140, 40, 0.10),
        transparent 70%
    );

    box-shadow:
        0 0 50px rgba(255, 100, 0, 0.22);

    animation:
        floatOrb 4s ease-in-out infinite;
}


/* =====================================================
   ANIMATIONS
===================================================== */

@keyframes slideRight {

    from {
        opacity: 0;
        transform: translateX(30px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}


@keyframes slideLeft {

    from {
        opacity: 0;
        transform: translateX(-30px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}


@keyframes fadeDown {

    from {
        opacity: 0;
        transform: translateY(-15px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


@keyframes cardAppear {

    from {
        opacity: 0;
        transform: translateY(15px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


@keyframes floatOrb {

    0%, 100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-12px);
    }
}


</style>
""", unsafe_allow_html=True)


# =========================================================
# GROQ MODEL
# =========================================================

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.9
)


# =========================================================
# PERSONALITY MODES
# =========================================================

modes = {

    "Angry Mode": {

        "prompt":
        "You are an angry AI agent. "
        "You respond aggressively and impatiently.",

        "description":
        "Responds aggressively and impatiently."
    },


    "Funny Mode": {

        "prompt":
        "You are a very funny AI agent. "
        "You respond with humor and jokes.",

        "description":
        "Responds with humor and jokes."
    },


    "Sad Mode": {

        "prompt":
        "You are a sad AI agent. "
        "You respond sadly and emotionally.",

        "description":
        "Responds sadly and with grief."
    }
}


# =========================================================
# MAIN LAYOUT
# =========================================================

left_col, right_col = st.columns(
    [1, 2.8],
    gap="large"
)


# =========================================================
# LEFT SIDE
# =========================================================

with left_col:

    st.markdown(
        """
<div class="app-title">
AI Mood <span>Chat</span>
</div>

<div class="app-subtitle">
Choose your AI personality
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="mode-label">
CHOOSE AI MODE
</div>
""",
        unsafe_allow_html=True
    )

    selected_mode = st.radio(
        "Select Mode",
        list(modes.keys()),
        label_visibility="collapsed"
    )

    # MODE CARDS

    for mode_name, details in modes.items():

        active_class = ""

        if mode_name == selected_mode:

            active_class = "active-mode"

        st.markdown(
            f"""
<div class="mode-card {active_class}">

<div class="mode-title">
{mode_name}
</div>

<div class="mode-description">
{details["description"]}
</div>

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown(
        """
<div class="orb"></div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# INITIALIZE CHAT
# =========================================================

current_prompt = modes[selected_mode]["prompt"]


if "messages" not in st.session_state:

    st.session_state.messages = [

        SystemMessage(
            content=current_prompt
        )

    ]

    st.session_state.current_mode = selected_mode


# =========================================================
# RESET CHAT WHEN MODE CHANGES
# =========================================================

if st.session_state.current_mode != selected_mode:

    st.session_state.messages = [

        SystemMessage(
            content=current_prompt
        )

    ]

    st.session_state.current_mode = selected_mode

    st.rerun()


# =========================================================
# RIGHT SIDE CHAT
# =========================================================

with right_col:

    st.markdown(
        f"""
<div class="chat-header">

<div class="chat-title">
Chat with <span>{selected_mode}</span>
</div>

<div class="chat-subtitle">
Your AI personality is ready.
</div>

</div>
""",
        unsafe_allow_html=True
    )

    # =====================================================
    # DISPLAY OLD MESSAGES
    # =====================================================

    for message in st.session_state.messages:

        if isinstance(message, HumanMessage):

            safe_content = html.escape(message.content)

            safe_content = safe_content.replace(
                "\n",
                "<br>"
            )

            st.markdown(
                f"""
<div class="user-message">

<div class="user-bubble">
{safe_content}
</div>

</div>
""",
                unsafe_allow_html=True
            )

        elif isinstance(message, AIMessage):

            safe_content = html.escape(message.content)

            safe_content = safe_content.replace(
                "\n",
                "<br>"
            )

            st.markdown(
                f"""
<div class="ai-message">

<div class="ai-bubble">
{safe_content}
</div>

</div>
""",
                unsafe_allow_html=True
            )

    # =====================================================
    # USER INPUT
    # =====================================================

    prompt = st.chat_input(
        "Type your message..."
    )

    if prompt:

        # Store user message first

        st.session_state.messages.append(
            HumanMessage(
                content=prompt
            )
        )

        # Generate AI response

        with st.spinner("Thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

        # Store AI response

        st.session_state.messages.append(
            AIMessage(
                content=response.content
            )
        )

        # Rerun so messages appear correctly
        # and avoid duplicate display

        st.rerun()


# =========================================================
# CLEAR CHAT BUTTON
# =========================================================

with left_col:

    if st.button("Clear Chat"):

        st.session_state.messages = [

            SystemMessage(
                content=modes[selected_mode]["prompt"]
            )

        ]

        st.rerun()
