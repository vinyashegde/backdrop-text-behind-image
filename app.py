import os
from flask import Flask, render_template, request, jsonify
from rembg import remove, new_session
import base64

app = Flask(__name__)
application = app  # For compatibility with some platforms (e.g. WSGI servers)

# Set the custom model path in your project directory
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.environ['U2NET_HOME'] = MODEL_DIR  # Set the environment variable for rembg to use

# Create a custom session for the 'u2netp' model
custom_session = new_session("u2netp")

@app.route('/')
def index():
    # Render the main HTML page
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if an image file is uploaded
    uploaded_file = request.files['image']
    if uploaded_file.filename != '':
        # Read the uploaded image file
        input_image = uploaded_file.read()
        
        # Process image to remove background using the custom session
        output_image = remove(input_image, session=custom_session)
        
        # Convert the original image and background-removed image to base64
        original_image_base64 = base64.b64encode(input_image).decode('utf-8')
        modified_image_base64 = base64.b64encode(output_image).decode('utf-8')
        
        # Send the images as JSON to the frontend
        return jsonify({
            'original_image': f'data:image/png;base64,{original_image_base64}',
            'background_removed_image': f'data:image/png;base64,{modified_image_base64}'
        })
    
    # Return an error if no image was uploaded
    return jsonify({'error': 'No image uploaded'}), 400

if __name__ == '__main__':
    # Use the port provided by Render (or default to 5000 for local development)
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port), debug=True)  # Listen on all interfaces (0.0.0.0)
