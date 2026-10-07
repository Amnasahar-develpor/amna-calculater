import streamlit as st

# Page Configuration
st.set_page_config(page_title="Neon Calculator", layout="centered")

# Custom CSS for Neon Background, Yellow Buttons, and Maroon Display Text
st.markdown("""
    <style>
    /* Neon Dark Background */
    .stApp {
        background-color: #050e14;
        color: #ffffff;
    }
    
    /* Display Screen styling with Maroon Text */
    .display-screen {
        background-color: #0d1b2a;
        color: #800020; /* Maroon Display Color */
        font-size: 52px;
        text-align: right;
        padding: 20px;
        font-weight: bold;
        min-height: 90px;
        word-wrap: break-word;
        border: 2px solid #00f3ff;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
        margin-bottom: 20px;
    }

    /* Base style for all buttons: Neon Yellow */
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 28px !important;
        border-radius: 50% !important;
        border: 2px solid #ffe600 !important;
        background-color: #121212 !important;
        color: #ffe600 !important; /* Neon Yellow Text */
        font-weight: bold !important;
        box-shadow: 0 0 8px rgba(255, 230, 0, 0.4);
    }

    /* Clear Button Red Color */
    div.stButton > button[data-testid="baseButton-secondary"]:nth-child(1) {
        color: #ff3366 !important;
        border-color: #ff3366 !important;
    }

    /* Equal Button Filled Neon Yellow */
    .equal-btn div.stButton > button {
        background-color: #ffe600 !important;
        color: #000000 !important;
        border-radius: 20px !important;
        box-shadow: 0 0 15px rgba(255, 230, 0, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

# Session State for Calculation
if "expression" not in st.session_state:
    st.session_state.expression = ""

def btn_click(symbol):
    if symbol == "C":
        st.session_state.expression = ""
    elif symbol == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
    elif symbol == "=":
        try:
            expr = st.session_state.expression.replace('%', '/100*').replace('×', '*').replace('÷', '/')
            st.session_state.expression = str(eval(expr))
        except Exception:
            st.session_state.expression = "Error"
    else:
        if st.session_state.expression == "Error":
            st.session_state.expression = ""
        st.session_state.expression += str(symbol)

# Display Screen (Maroon Text)
display_text = st.session_state.expression if st.session_state.expression else "0"
st.markdown(f'<div class="display-screen">{display_text}</div>', unsafe_allow_html=True)

# Grid Layout: 4 Columns per row (Normal Calculator Layout)
buttons = [
    ['C', '%', '⌫', '÷'],
    ['7', '8', '9', '×'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['🎨', '0', '.', '=']
]

# Render Calculator Buttons
for row in buttons:
    cols = st.columns(4)
    for col, btn in zip(cols, row):
        with col:
            if btn == '=':
                st.markdown('<div class="equal-btn">', unsafe_allow_html=True)
                if st.button(btn, key=f"btn_{btn}"):
                    btn_click(btn)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button(btn, key=f"btn_{btn}"):
                    btn_click(btn)
