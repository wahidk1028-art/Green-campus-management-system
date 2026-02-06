import streamlit as st
import sqlite3
import pandas as pd
import os
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Waste Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;'>♻️ AI Waste Segregation Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Green Campus Management System</h4>", unsafe_allow_html=True)
st.divider()

# ---------------- LOAD DATABASE ----------------
conn = sqlite3.connect("waste_log.db")
df = pd.read_sql("SELECT * FROM waste_log", conn)
conn.close()

if df.empty:
    st.warning("No waste data available.")
    st.stop()

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Waste Types", df['waste_type'].nunique())
col3.metric("Last Detected Waste", df.iloc[-1]['waste_type'])

st.divider()

# ---------------- TABLE ----------------
st.subheader("📋 Waste Detection Records")
st.dataframe(df, use_container_width=True)

st.divider()

# ---------------- CHARTS ----------------
waste_count = df['waste_type'].value_counts()

col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Waste Distribution")
    st.bar_chart(waste_count)

with col5:
    st.subheader("🥧 Waste Percentage")
    st.pyplot(waste_count.plot(kind='pie', autopct='%1.1f%%').figure)

st.divider()

# ---------------- IMAGE GALLERY ----------------
st.subheader("📸 Captured Waste Images")

image_folder = "captured_images"
images = os.listdir(image_folder) if os.path.exists(image_folder) else []

if not images:
    st.info("No images captured yet.")
else:
    cols = st.columns(4)
    for i, img_name in enumerate(images):
        img_path = os.path.join(image_folder, img_name)
        img = Image.open(img_path)

        with cols[i % 4]:
            st.image(img, caption=img_name, use_column_width=True)
            if st.button(f"View {img_name}", key=img_name):
                st.session_state["selected_img"] = img_path

# ---------------- IMAGE VIEWER ----------------
if "selected_img" in st.session_state:
    st.divider()
    st.subheader("🔍 Selected Image Preview")
    st.image(st.session_state["selected_img"], use_column_width=True)

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align:center;'>AI-based Smart Waste Management System</p>",
    unsafe_allow_html=True
)
