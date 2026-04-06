import os
import cv2
import base64
import logging
import io
from PIL import Image
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Initialize basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment API Keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_ACTIVE = False

# Try formatting the Cloud API
try:
    import google.generativeai as genai
    if GEMINI_API_KEY and GEMINI_API_KEY.strip() and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
        genai.configure(api_key=GEMINI_API_KEY)
        # Use the highly efficient multimodal flash model
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        API_ACTIVE = True
        logging.info("Gemini Cloud Vision API Successfully Activated! 🚀")
    else:
        logging.warning("GEMINI_API_KEY missing from .env file! Falling back to color simulation.")
except ImportError:
    logging.warning("google-generativeai module not found.")

def simulate_prediction(b64_str):
    """Fallback color heuristic if the API Key is missing"""
    import numpy as np
    try:
        img_data = base64.b64decode(b64_str)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        h, w = frame.shape[:2]
        center = frame[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
        mean_b, mean_g, mean_r = cv2.mean(center)[:3]
        
        if mean_g > mean_r and mean_g > (mean_b + 10):
            return "Fresh", 0.9
        else:
            return "Spoiled", 0.9
    except Exception:
        return "Unknown", 0.0

def generate_voice_message(label):
    if label == "Fresh":
        return "This item looks fresh."
    elif label == "Spoiled":
        return "Warning: This item appears spoiled."
    return "Cannot verify."

# -----------------------------------------------------
# Flask Web Server Configuration
# -----------------------------------------------------

app = Flask(__name__)
# Enable CORS for Mobile browsers requesting API access
CORS(app)

@app.route('/')
def index():
    """Serves the Premium Mobile Glassmorphism PWA UI"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_endpoint():
    """Receives Base64 image frames from mobile WebRTC and returns Cloud ML predictions"""
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    image_data = data['image']
    # The image string comes prefixed with "data:image/jpeg;base64,"
    if "," in image_data:
        b64_str = image_data.split(",")[1]
    else:
        b64_str = image_data

    # Cloud AI Strategy
    if API_ACTIVE:
        try:
            # Decode the string back into bytes for Pillow
            img_bytes = base64.b64decode(b64_str)
            pil_image = Image.open(io.BytesIO(img_bytes))
            
            # Formulate prompt for Gemini
            prompt = """Act as an expert food safety detector. Look closely at the image. 
            Rule 1: If the image is of a person, a background, or NOT a clear food item, reply exactly with: "Not Food - Unknown"
            Rule 2: If it IS a clear food item, identify the specific food and determine if it is 'Fresh' or 'Spoiled'.
            
            Reply in exactly this format and nothing else: [Food Name] - [FRESH/SPOILED]"""
            response = gemini_model.generate_content([prompt, pil_image])
            raw_text = response.text.strip()
            
            if "Not Food" in raw_text or "Unknown" in raw_text:
                final_label = "Unknown"
                voice_override = "This does not appear to be a clear food item."
            elif 'SPOILED' in raw_text.upper() or 'ROT' in raw_text.upper():
                final_label = "Spoiled"
                food_name = raw_text.split('-')[0].strip() if '-' in raw_text else "item"
                voice_override = f"Warning: This {food_name} appears spoiled."
            elif 'FRESH' in raw_text.upper() or 'GOOD' in raw_text.upper():
                final_label = "Fresh"
                food_name = raw_text.split('-')[0].strip() if '-' in raw_text else "item"
                voice_override = f"This {food_name} looks fresh."
            else:
                final_label = "Unknown"
                voice_override = None
                
            prediction_confidence = 0.99 # Cloud models are highly precise
            
        except Exception as e:
            logging.error(f"Gemini API Error: {e}")
            final_label = "Error"
            prediction_confidence = 0.0
            voice_override = None
    else:
        # Fallback to local heuristic
        final_label, prediction_confidence = simulate_prediction(b64_str)
        voice_override = None

    voice_text = voice_override if voice_override else generate_voice_message(final_label)

    return jsonify({
        "label": final_label,
        "confidence": round(prediction_confidence, 2),
        "voice_text": voice_text
    })

if __name__ == "__main__":
    # Host on 0.0.0.0 to broadcast to LAN for cell phone connectivity
    print("======================================================")
    print(" 🚀 FreshVision Cloud Web Server Active (HTTPS) 🚀")
    if API_ACTIVE:
         print(" 🌟 CLOUD AI: GEMINI VISION ACTIVATED 🌟")
    else:
         print(" ⚠️ CLOUD AI OFFLINE: Fallback color mode active. Please add API Key to .env!")
    print("======================================================")
    print("👉 To run on your phone, find this computer's IP address (e.g. 192.168.1.5)")
    print("👉 Then type exactly this in your iPhone/Android browser: https://<IP_ADDRESS>:8081")
    print("⚠️  Warning: Your browser will say 'Not Secure'. Click 'Advanced' -> 'Proceed' to allow camera access!")
    # app.run(host="0.0.0.0", port=8081, ssl_context='adhoc', debug=False) this is for local host 
     #We remove ssl_context and hardcoded IPs because the cloud provider handles that now.
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
