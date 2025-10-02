"""
WT_CARBON_SCOPE_COMPASS

"""
#cdm
#     projenv\Scripts\activate
#     streamlit run home.py

import streamlit as st
import pandas as pd


# ✅ Must be the first Streamlit call
st.set_page_config(
    page_title="Home",   # Browser tab title
    page_icon="🏠",      # Optional favicon (emoji or path to .png/.ico)
    layout="wide"        # "centered" or "wide"
)


# ── Load user credentials and profiles ────────────────────────
CREDENTIALS = dict(st.secrets["auth"])
PROFILES = st.secrets.get("profile", {})

# ── Login form ────────────────────────────────────────────────
def login():
    st.title("🔐 Login Required")

    user = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login", key="login_button"):
        if user in CREDENTIALS and password == CREDENTIALS[user]:
            st.session_state["authenticated"] = True
            st.session_state["username"] = user
            st.session_state["first_name"] = PROFILES.get(user, {}).get("first_name", user)
        else:
            st.error("❌ Invalid username or password")

# ── Auth state setup ──────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ── Login gate ────────────────────────────────────────────────
if not st.session_state["authenticated"]:
    login()
    st.stop()

# ── App begins after login ────────────────────────────────────

# ---------------Sidebar
from utils import apply_style_and_logo

st.sidebar.success(f"Welcome {st.session_state['first_name']}!")
st.sidebar.button("Logout", on_click=lambda: st.session_state.update(authenticated=False))

# Spacer to push the link to the bottom (optional tweak for better placement)
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Company website link
st.sidebar.markdown(
    '<p style="text-align:center;">'
    '<a href="https://www.wavetransition.com" target="_blank">🌐 Visit WaveTransition</a>'
    '</p>',
    unsafe_allow_html=True
)
# ---------Main content
st.set_page_config(page_title="Fuel Dashboard", layout="wide")

# --- Centered cover image ---
from PIL import Image
cover_img = Image.open("cover.png")
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image(cover_img, use_container_width=False, width=800)  # updated
#st.image(cover_img, use_container_width=True)  # auto fit


st.markdown("</div>", unsafe_allow_html=True)

st.title("**CARBON SCOPE COMPASS**")
st.markdown("""
## 🧭 CarbonScope Navigator  
*Your directional tool for EU ETS & CBAM cost and compliance strategy*

---

### 🌍 Coverage: EU ETS Phase 4, CBAM & ETS2 (Road & Buildings)

This app provides **company-level insights** into emissions reporting, allowance allocations, and regulatory costs under the evolving EU carbon pricing framework.  
It covers key aspects of:

- 🏭 **EU ETS Phase 4 installations** and allocation trends  
- 🛢️ **ETS2 sector entry** (road transport & buildings)  
- 🏗️ **CBAM-exposed sectors** (steel, cement, aluminum, etc.) and import exposure  
- 💶 **Carbon cost impacts** based on verified emissions and market price assumptions

---

### 🎯 Purpose

**CarbonScope Navigator** is built for **consultants and company advisors**.  
It offers a **fast, harmonized view** of EU carbon regulations — helping organizations:

- Understand their **exposure under EU ETS and CBAM**
- Estimate **financial impacts of allowance deficits**
- Navigate upcoming **compliance risks and obligations**
- Support **strategic decision-making** (procurement, investment, partnerships)

---

### 🔍 Key Features

- 📊 **Visual comparison** of allowance vs. verified emissions  
- 🧾 **ETS cost estimator** using dynamic CO₂ price inputs  
- 🏷️ **Interactive filtering** by country, sector, or installation  
- 🗂️ **Company-level data download** and PDF/HTML export  
- 📈 Optional **trend views**, surplus/deficit classification, and CBAM overlays  

---

### ⚠️ Note

This tool is designed for **preliminary analysis and strategic screening**.  
For technical reporting, compliance filing, or CBAM import calculations, use official EC sources and methodologies.

---

### 🚀 Start exploring!

Use the sidebar to **select your country, activity, and year**, then dive into **interactive plots**, **cost estimates**, and **emission gap diagnostics**.

""")

