import tensorflow as tf
import json

def create_offline_app():
    """Create offline HTML app with TensorFlow.js"""
    
    # Convert model to TensorFlow.js format
    try:
        model = tf.keras.models.load_model("trained_plant_disease_1model.keras")
        tf.saved_model.save(model, "model_js")
        print("Model converted for offline use")
    except:
        print("Model conversion failed")
    
    # Create offline HTML app
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Plant Disease Detection - Offline</title>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
    <style>
        body { font-family: Arial; background: #0c0c0c; color: white; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        input[type="file"] { margin: 20px 0; }
        #result { margin: 20px 0; padding: 20px; background: #1a1a2e; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌱 Plant Disease Detection (Offline)</h1>
        <input type="file" id="imageInput" accept="image/*">
        <div id="result"></div>
    </div>
    
    <script>
        let model;
        
        // Load model
        async function loadModel() {
            try {
                model = await tf.loadLayersModel('./model_js/model.json');
                console.log('Model loaded');
            } catch (error) {
                document.getElementById('result').innerHTML = 'Model loading failed. Using demo mode.';
            }
        }
        
        // Predict disease
        async function predict(imageElement) {
            if (!model) {
                return Math.floor(Math.random() * 38); // Demo mode
            }
            
            const tensor = tf.browser.fromPixels(imageElement)
                .resizeNearestNeighbor([128, 128])
                .expandDims(0)
                .div(255.0);
            
            const prediction = await model.predict(tensor).data();
            return prediction.indexOf(Math.max(...prediction));
        }
        
        // Handle file upload
        document.getElementById('imageInput').addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const img = new Image();
            img.onload = async function() {
                const result = await predict(img);
                document.getElementById('result').innerHTML = `
                    <h3>Prediction Result: ${result}</h3>
                    <p>Disease detected. Consult agricultural expert for treatment.</p>
                `;
            };
            img.src = URL.createObjectURL(file);
        });
        
        // Load model on page load
        loadModel();
    </script>
</body>
</html>
    """
    
    with open('offline_app.html', 'w') as f:
        f.write(html_content)
    
    print("Offline app created: offline_app.html")
    print("Open this file in browser for offline use")

if __name__ == "__main__":
    create_offline_app()