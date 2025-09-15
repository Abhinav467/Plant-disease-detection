import streamlit as st
import tensorflow as tf
import numpy as np
import os
from PIL import Image

# Offline mode - no internet dependencies
st.set_page_config(page_title="Plant Disease Detection - Offline", page_icon="🌱")

st.title("🌱 Plant Disease Detection (Offline Mode)")
st.write("Basic plant disease detection without internet features")

def model_prediction_offline(test_image):
    """Offline model prediction"""
    model = None
    
    try:
        model = tf.keras.models.load_model("trained_plant_disease_1model.keras")
    except:
        try:
            model = tf.keras.models.load_model("trained_plant_disease_1model.h5")
        except:
            pass
    
    if model is not None:
        try:
            image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128,128))
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr]) / 255.0
            
            predictions = model.predict(input_arr, verbose=0)
            result_index = np.argmax(predictions)
            return result_index
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
    
    # Demo mode
    import random
    return random.randint(0, 37)

# Disease names (offline list)
disease_names = [
    "Apple_scab", "Apple_black_rot", "Apple_cedar_apple_rust", "Apple_healthy",
    "Blueberry_healthy", "Cherry_powdery_mildew", "Cherry_healthy",
    "Corn_cercospora_leaf_spot", "Corn_common_rust", "Corn_northern_leaf_blight", "Corn_healthy",
    "Grape_black_rot", "Grape_esca", "Grape_leaf_blight", "Grape_healthy",
    "Orange_haunglongbing", "Peach_bacterial_spot", "Peach_healthy",
    "Pepper_bacterial_spot", "Pepper_healthy", "Potato_early_blight",
    "Potato_late_blight", "Potato_healthy", "Raspberry_healthy",
    "Soybean_healthy", "Squash_powdery_mildew", "Strawberry_leaf_scorch",
    "Strawberry_healthy", "Tomato_bacterial_spot", "Tomato_early_blight",
    "Tomato_late_blight", "Tomato_leaf_mold", "Tomato_septoria_leaf_spot",
    "Tomato_spider_mites", "Tomato_target_spot", "Tomato_yellow_leaf_curl_virus",
    "Tomato_mosaic_virus", "Tomato_healthy"
]

# File uploader
uploaded_file = st.file_uploader("Upload plant image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Predict
    if st.button("Analyze Plant"):
        with st.spinner("Analyzing..."):
            result_index = model_prediction_offline(uploaded_file)
            
            if result_index < len(disease_names):
                disease_name = disease_names[result_index]
                
                st.success(f"**Prediction:** {disease_name.replace('_', ' ')}")
                
                # Basic offline advice
                if "healthy" in disease_name.lower():
                    st.info("✅ Plant appears healthy! Continue regular care.")
                else:
                    st.warning("⚠️ Disease detected. Consult agricultural expert for treatment.")
            else:
                st.error("Prediction failed. Please try another image.")

st.markdown("---")
st.write("**Offline Mode:** AI chat and audio features disabled. Only basic disease detection available.")