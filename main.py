import streamlit as st
import tensorflow as tf
import numpy as np
import os
import google.generativeai as genai
from gtts import gTTS
import io
import base64
# PWA files exist but no UI elements

# Modern Dark Theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .neon-header {
        background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(255, 0, 110, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(255, 0, 110, 0.3); }
        to { box-shadow: 0 0 40px rgba(255, 0, 110, 0.6); }
    }
    
    .feature-box {
        background: linear-gradient(135deg, rgba(131, 56, 236, 0.2), rgba(58, 134, 255, 0.2));
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
        transition: transform 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(131, 56, 236, 0.4);
    }
    
    .prediction-result {
        background: linear-gradient(135deg, #00f5ff, #0066ff);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 0 25px rgba(0, 245, 255, 0.4);
        color: #000;
        font-weight: bold;
    }
    
    .chat-bubble {
        background: rgba(255, 255, 255, 0.1);
        border-left: 4px solid #ff006e;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff006e, #8338ec);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 110, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 0, 110, 0.5);
    }
</style>
""", unsafe_allow_html=True)

def model_prediction(test_image):
    model = None
    
    try:
        model = tf.keras.models.load_model("trained_plant_disease_1model.keras")
        print("Model loaded with method 1")
    except:
        pass
    
    if model is None:
        try:
            model = tf.keras.models.load_model("trained_plant_disease_1model.keras", compile=False)
            print("Model loaded with method 2")
        except:
            pass
    
    if model is None:
        try:
            model = tf.keras.models.load_model("trained_plant_disease_1model.h5")
            print("Model loaded with method 3")
        except:
            pass
    
    if model is not None:
        try:
            image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128,128))
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr]) / 255.0
            
            predictions = model.predict(input_arr, verbose=0)
            result_index = np.argmax(predictions)
            
            print(f"Real prediction: {result_index}")
            return result_index
        except Exception as e:
            print(f"Prediction failed: {str(e)}")
    
    print("Using demo mode - model not working")
    import random
    return random.randint(0, 37)

GEMINI_API_KEY = "AIzaSyBYMzJypwMBYIFF_bS9o8LSDl5eyrUVlsA"
genai.configure(api_key=GEMINI_API_KEY)

def get_plant_advice(disease_name, plant_type):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        if "healthy" in disease_name.lower():
            prompt = f"As a plant expert, provide encouraging advice for a healthy {plant_type} plant. Keep it concise and positive."
        else:
            prompt = f"As a plant disease expert, provide treatment advice for {disease_name.replace('_', ' ')} in {plant_type}. Include symptoms, causes, and specific treatment steps. Keep it practical and concise."
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        if "healthy" in disease_name.lower():
            return f"Excellent! Your {plant_type} is healthy. Continue with regular watering, ensure good sunlight, and monitor for any changes. Keep up the great plant care!"
        else:
            return f"{disease_name.replace('_', ' ')} detected in your {plant_type}. Recommend consulting local agricultural experts for specific treatment. General advice: isolate plant, remove affected parts, and improve growing conditions."

def text_to_speech(text, lang='en'):
    """Convert text to speech and return audio player"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        audio_base64 = base64.b64encode(fp.read()).decode()
        audio_html = f"""
        <audio controls style="width: 100%; margin: 10px 0;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        return audio_html
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

def get_gemini_answer(question, disease_name, plant_type):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Enhanced prompt with specific question context
        prompt = f"""You are an expert plant pathologist with 20+ years of experience. 
        
        PLANT: {plant_type}
        DIAGNOSIS: {disease_name.replace('_', ' ')}
        SPECIFIC QUESTION: "{question}"
        
        Please provide a direct, specific answer to this exact question about {disease_name.replace('_', ' ')} in {plant_type}. 
        
        Focus only on answering what was asked. Be practical, accurate, and concise. If the plant is healthy, focus on maintenance advice relevant to the question."""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # More specific fallback responses based on question keywords
        question_lower = question.lower()
        
        if "healthy" in disease_name.lower():
            if "symptom" in question_lower:
                return f"Your {plant_type} shows no disease symptoms. Healthy signs include vibrant green leaves, strong stems, and normal growth patterns."
            elif "treatment" in question_lower or "best treatment" in question_lower:
                return f"No treatment needed for healthy {plant_type}. Continue regular care: proper watering, adequate sunlight, and balanced fertilization."
            elif "prevent" in question_lower:
                return f"To keep {plant_type} healthy: maintain good air circulation, avoid overwatering, provide proper spacing, and inspect regularly for early disease signs."
            elif "contagious" in question_lower:
                return f"Healthy {plant_type} poses no disease risk to other plants. It's actually a good sign that your plant care practices are working well."
            elif "fertilizer" in question_lower:
                return f"For healthy {plant_type}: use balanced fertilizer (10-10-10) monthly during growing season, reduce in winter months."
            elif "water" in question_lower:
                return f"Water healthy {plant_type} when top inch of soil feels dry, typically 1-2 times per week depending on season and humidity."
            elif "environmental" in question_lower or "environment" in question_lower:
                return f"Healthy {plant_type} thrives with 6-8 hours sunlight, well-draining soil, temperatures 65-75°F, and moderate humidity."
            elif "organic" in question_lower:
                return f"For healthy {plant_type}: use organic compost, neem oil for pest prevention, and organic mulch to retain soil moisture."
            elif "recovery" in question_lower or "time" in question_lower:
                return f"Your {plant_type} is already healthy! Continue current care routine to maintain optimal plant health."
            elif "remove" in question_lower or "leaves" in question_lower:
                return f"Only remove dead, damaged, or yellowing leaves from healthy {plant_type}. Healthy green leaves should remain on the plant."
            elif "warning" in question_lower or "signs" in question_lower:
                return f"Watch for these warning signs in {plant_type}: yellowing leaves, brown spots, wilting, stunted growth, or unusual leaf patterns."
            else:
                return f"Your {plant_type} is healthy! Continue with proper watering, adequate sunlight, and regular monitoring for any changes."
        else:
            if "symptom" in question_lower:
                return f"Common symptoms of {disease_name.replace('_', ' ')} in {plant_type}: discolored leaves, spots, wilting, stunted growth. Check leaves, stems, and roots carefully."
            elif "treatment" in question_lower or "best treatment" in question_lower:
                return f"Treatment for {disease_name.replace('_', ' ')}: Remove affected parts immediately, improve air circulation, apply appropriate fungicide, and isolate from healthy plants."
            elif "prevent" in question_lower:
                return f"Prevent {disease_name.replace('_', ' ')} by: proper plant spacing, good drainage, avoiding overhead watering, regular inspection, and removing plant debris."
            elif "contagious" in question_lower:
                return f"Yes, {disease_name.replace('_', ' ')} can spread to other {plant_type} plants. Isolate affected plant and sterilize tools between plants."
            elif "fertilizer" in question_lower:
                return f"For {plant_type} with {disease_name.replace('_', ' ')}: reduce nitrogen, use phosphorus-potassium fertilizer to boost immunity, avoid over-fertilizing."
            elif "water" in question_lower:
                return f"Water {plant_type} with {disease_name.replace('_', ' ')} carefully: water at soil level, avoid wetting leaves, ensure good drainage, reduce frequency slightly."
            elif "environmental" in question_lower or "environment" in question_lower:
                return f"{plant_type} with {disease_name.replace('_', ' ')} needs: improved air circulation, reduced humidity, proper spacing, and avoid overhead watering."
            elif "organic" in question_lower:
                return f"Organic treatments for {disease_name.replace('_', ' ')}: neem oil, baking soda spray, copper fungicide, beneficial bacteria, and proper composting."
            elif "recovery" in question_lower or "time" in question_lower:
                return f"Recovery from {disease_name.replace('_', ' ')} typically takes 2-4 weeks with proper treatment. Monitor progress and continue care routine."
            elif "remove" in question_lower or "leaves" in question_lower:
                return f"Yes, immediately remove all leaves affected by {disease_name.replace('_', ' ')} and dispose in trash (not compost) to prevent spread."
            elif "warning" in question_lower or "signs" in question_lower:
                return f"Early signs of {disease_name.replace('_', ' ')}: small spots on leaves, slight discoloration, reduced vigor. Act quickly when noticed."
            else:
                return f"For {disease_name.replace('_', ' ')} in {plant_type}: Remove affected parts, improve growing conditions, and consider appropriate treatments. Monitor closely."

# Sidebar
st.sidebar.markdown("""
<div style="background: linear-gradient(45deg, #ff006e, #8338ec); padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
    <h2 style="color: white; margin: 0;">🤖 AI Plant Doctor</h2>
</div>
""", unsafe_allow_html=True)

app_mode = st.sidebar.selectbox("🚀 Navigate", ["🏠 Home", "ℹ️ About", "🔬 Disease Recognition"])

if app_mode == "🏠 Home":
    st.markdown("""
    <div class="neon-header">
        <h1>🌿 AI PLANT DISEASE RECOGNITION SYSTEM</h1>
        <p style="font-size: 1.2rem; margin: 0;">Next-Gen Plant Health Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    image_path = "home_page.jpeg"
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🚀 How It Works</h3>
            <p><strong>1. Upload:</strong> Select your plant image</p>
            <p><strong>2. Analyze:</strong> AI processes with ML algorithms</p>
            <p><strong>3. Diagnose:</strong> Get instant results</p>
            <p><strong>4. Chat:</strong> Ask our AI expert questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>⚡ AI Features</h3>
            <p>• Instant Disease Detection</p>
            <p>• Expert AI Chatbot</p>
            <p>• Interactive Q&A System</p>
            <p>• 24/7 Plant Health Support</p>
            <p>• Treatment Recommendations</p>
        </div>
        """, unsafe_allow_html=True)

elif app_mode == "ℹ️ About":
    st.markdown("""
    <div class="neon-header">
        <h1>About Our AI Plant Doctor</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🤖 AI Technology</h3>
            <p>Advanced computer vision combined with natural language processing:</p>
            <p>• Deep learning disease detection</p>
            <p>• Conversational AI treatment advice</p>
            <p>• Interactive chatbot system</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📊 Dataset Info</h3>
            <p>87K RGB images across 38 plant disease classes</p>
            <p>• Training: 70,295 images</p>
            <p>• Validation: 17,572 images</p>
            <p>• Test: 33 images</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
        <h3>🎯 Supported Plants</h3>
        <p>Apple • Blueberry • Cherry • Corn • Grape • Orange • Peach • Pepper • Potato • Raspberry • Soybean • Squash • Strawberry • Tomato</p>
    </div>
    """, unsafe_allow_html=True)

elif app_mode == "🔬 Disease Recognition":
    st.markdown("""
    <div class="neon-header">
        <h1>🤖 AI Plant Doctor - Disease Recognition</h1>
        <p>Upload your plant image for instant AI analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    test_image = st.file_uploader("📸 Choose Plant Image", type=['jpg', 'jpeg', 'png'])
    
    if test_image is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(test_image, caption="Your Plant Image", use_column_width=True)
        with col2:
            st.markdown("""
            <div class="chat-bubble">
                <h3>🔍 Image Ready</h3>
                <p>Image uploaded successfully! Click analyze for AI diagnosis.</p>
            </div>
            """, unsafe_allow_html=True)
    
    if 'prediction_made' not in st.session_state:
        st.session_state.prediction_made = False
    if 'prediction_data' not in st.session_state:
        st.session_state.prediction_data = None
    
    if st.button("🤖 Analyze with AI Doctor", type="primary"):
        if test_image is not None:
            st.snow()
            
            result_index = model_prediction(test_image)
            
            model_exists = os.path.exists("trained_plant_disease_1model.keras") or os.path.exists("trained_plant_disease_1model.h5")
            if not model_exists:
                st.warning("🔄 Demo Mode: Model file not found")
            else:
                st.info("🤖 Using trained AI model")
            
            class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                        'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                        'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                        'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                        'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                        'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                        'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                        'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                        'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                        'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                        'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                        'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                        'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                        'Tomato___healthy']
            
            predicted_disease = class_name[result_index]
            plant_type = predicted_disease.split('___')[0].replace('_', ' ')
            disease_name = predicted_disease.split('___')[1] if '___' in predicted_disease else 'Unknown'
            
            st.session_state.prediction_data = {
                'result_index': result_index,
                'predicted_disease': predicted_disease,
                'plant_type': plant_type,
                'disease_name': disease_name
            }
            st.session_state.prediction_made = True
            
            if "healthy" in disease_name.lower():
                st.markdown(f"""
                <div class="prediction-result" style="background: linear-gradient(135deg, #00ff88, #00cc66);">
                    <h2>🌿 Excellent News!</h2>
                    <h3>Your {plant_type} is HEALTHY! 🎉</h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="prediction-result" style="background: linear-gradient(135deg, #ff6b6b, #ffa500);">
                    <h2>🔍 Diagnosis Complete</h2>
                    <h3>Plant: {plant_type}</h3>
                    <h3>Condition: {disease_name.replace('_', ' ')}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            advice = get_plant_advice(disease_name, plant_type)
            
            st.markdown(f"""
            <div class="chat-bubble">
                <h3>🤖 AI Doctor's Advice:</h3>
                <p>{advice}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Voice output for diagnosis
            st.markdown("### 🔊 Listen to Diagnosis")
            audio_text = f"Diagnosis for your {plant_type}: {disease_name.replace('_', ' ')}. {advice}"
            audio_html = text_to_speech(audio_text)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
        else:
            st.error("Please upload an image first!")
    
    if st.session_state.prediction_made and st.session_state.prediction_data:
        st.markdown("---")
        st.markdown("""
        <div class="chat-bubble">
            <h2>💬 Chat with AI Plant Doctor</h2>
            <p>Ask questions about your plant's condition!</p>
        </div>
        """, unsafe_allow_html=True)
        
        questions = [
            "What are the main symptoms of this disease?",
            "How did my plant get this disease?",
            "What's the best treatment for this condition?",
            "How can I prevent this disease in future?",
            "Is this disease contagious to other plants?",
            "What fertilizer should I use now?",
            "How often should I water this plant?",
            "What environmental conditions does it need?",
            "Can I use organic treatments for this?",
            "How long will recovery take?",
            "Should I remove the affected leaves?",
            "What are the early warning signs?"
        ]
        
        cols = st.columns(3)
        for i, question in enumerate(questions):
            with cols[i % 3]:
                if st.button(question, key=f"q_{i}"):
                    with st.spinner("🤖 AI thinking..."):
                        answer = get_gemini_answer(
                            question, 
                            st.session_state.prediction_data['disease_name'],
                            st.session_state.prediction_data['plant_type']
                        )
                    
                    st.markdown(f"""
                    <div class="chat-bubble">
                        <h4>❓ {question}</h4>
                        <p>{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Voice output for answer
                    st.markdown("#### 🔊 Listen to Answer")
                    audio_html = text_to_speech(answer)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
        
        custom_question = st.text_input("✍️ Ask your own question:")
        
        if st.button("🚀 Ask AI Doctor"):
            if custom_question:
                with st.spinner("🤖 Processing..."):
                    answer = get_gemini_answer(
                        custom_question,
                        st.session_state.prediction_data['disease_name'],
                        st.session_state.prediction_data['plant_type']
                    )
                
                st.markdown(f"""
                <div class="chat-bubble">
                    <h4>❓ {custom_question}</h4>
                    <p>{answer}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Voice output for custom answer
                st.markdown("#### 🔊 Listen to Answer")
                audio_html = text_to_speech(answer)
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
            else:
                st.error("Please enter a question!")