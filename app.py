import streamlit as st
import cv2
import numpy as np
import sqlite3
import pandas as pd
import os
from PIL import Image
from tensorflow.keras.models import load_model
from db_handler import init_db, log_waste

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Waste Segregation",
    page_icon="♻️",
    layout="wide"
)

# ---------------- INIT ----------------
init_db()
model = load_model("waste_classifier.h5")
classes = ["metal", "paper", "plastic"]
IMG_SIZE = 150

os.makedirs("captured_images", exist_ok=True)

# ---------------- UI HEADER ----------------
st.markdown("<h1 style='text-align:center;'>♻️ AI Waste Segregation System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Green Campus Management System</h4>", unsafe_allow_html=True)
st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🔍 Detect Waste", "📊 Dashboard", "📸 Captured Images"])

# ---------------- DETECT WASTE ----------------
if page == "🔍 Detect Waste":
    st.subheader("Upload or Capture Waste Image")

    img_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Input Image", width=300)

        img = np.array(image)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img, verbose=0)
        class_index = np.argmax(prediction)
        waste_type = classes[class_index]
        confidence = prediction[0][class_index]

        st.success(f"Detected Waste: **{waste_type.upper()}**")
        st.info(f"Confidence: {confidence*100:.2f}%")

        if confidence > 0.85:
            log_waste(waste_type)

            save_path = f"captured_images/{waste_type}_{len(os.listdir('captured_images'))}.jpg"
            image.save(save_path)

            st.toast("Data saved successfully!")

# ---------------- DASHBOARD ----------------
elif page == "📊 Dashboard":
    st.subheader("Waste Detection Dashboard")

    conn = sqlite3.connect("waste_log.db")
    df = pd.read_sql("SELECT * FROM waste_log", conn)
    conn.close()

    if df.empty:
        st.warning("No data available.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Waste Types", df['waste_type'].nunique())
        col3.metric("Last Waste", df.iloc[-1]['waste_type'])

        st.divider()
        st.dataframe(df, use_container_width=True)

        st.divider()
        waste_count = df['waste_type'].value_counts()

        col4, col5 = st.columns(2)
        with col4:
            st.subheader("Waste Count")
            st.bar_chart(waste_count)

        with col5:
            st.subheader("Waste Percentage")
            st.pyplot(waste_count.plot(kind="pie", autopct="%1.1f%%").figure)

# ---------------- IMAGE GALLERY ----------------
elif page == "📸 Captured Images":
    st.subheader("Captured Waste Images")

    images = os.listdir("captured_images")

    if not images:
        st.info("No images captured yet.")
    else:
        cols = st.columns(4)
        for i, img_name in enumerate(images):
            img = Image.open(f"captured_images/{img_name}")
            with cols[i % 4]:
                st.image(img, caption=img_name, use_column_width=True)

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align:center;'>AI-Based Smart Waste Management System</p>",
    unsafe_allow_html=True
)
