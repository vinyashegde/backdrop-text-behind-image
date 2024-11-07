# app.py
import os
import requests
from flask import Flask, render_template, request, jsonify
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
application = app  # For compatibility with some platforms (e.g. WSGI servers)

# Get API keys from environment variables
API_KEYS = [
    os.getenv('REMOVE_BG_API_KEY_1'),
    os.getenv('REMOVE_BG_API_KEY_2'),
    os.getenv('REMOVE_BG_API_KEY_3'),
    os.getenv('REMOVE_BG_API_KEY_4'),
    os.getenv('REMOVE_BG_API_KEY_5'),
    os.getenv('REMOVE_BG_API_KEY_6'),
    os.getenv('REMOVE_BG_API_KEY_7'),
    os.getenv('REMOVE_BG_API_KEY_8'),
    os.getenv('REMOVE_BG_API_KEY_9'),
]

# List of API endpoints (in order of preference)
API_ENDPOINTS = [
    os.getenv('REMOVE_BG_API_ENDPOINT'),  # Primary API
    os.getenv('REMOVE_BG_API_ENDPOINT'),  # Fallback APIs (same endpoint, different keys)
    os.getenv('REMOVE_BG_API_ENDPOINT'),
    os.getenv('REMOVE_BG_API_ENDPOINT'),
    os.getenv('REMOVE_BG_API_ENDPOINT'),
    os.getenv('REMOVE_BG_API_ENDPOINT'),
    os.getenv('REMOVE_BG_API_ENDPOINT'),
    os.getenv('REMOVE_BG_API_ENDPOINT'),
    os.getenv('REMOVE_BG_API_ENDPOINT'),
]

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

        # Try each API in the list until one succeeds
        for api_key, api_endpoint in zip(API_KEYS, API_ENDPOINTS):
            try:
                response = requests.post(
                    api_endpoint,
                    files={'image_file': input_image},
                    data={'size': 'auto'},
                    headers={'X-Api-Key': api_key}
                )
                
                # If the request is successful, process the response
                if response.status_code == requests.codes.ok:
                    output_image = response.content  # The background-removed image
                    
                    # Convert the original image and background-removed image to base64
                    original_image_base64 = base64.b64encode(input_image).decode('utf-8')
                    modified_image_base64 = base64.b64encode(output_image).decode('utf-8')
                    
                    # Return the images as JSON to the frontend
                    return jsonify({
                        'original_image': f'data:image/png;base64,{original_image_base64}',
                        'background_removed_image': f'data:image/png;base64,{modified_image_base64}'
                    })
                else:
                    # Log error if API fails but continue to the next one
                    print(f"API failed with status {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                # Log the exception and continue to the next API in the list
                print(f"Request failed: {str(e)}")

        # If all APIs fail, return an error message
        return jsonify({'error': 'All APIs failed to process the image'}), 500

    # Return an error if no image was uploaded
    return jsonify({'error': 'No image uploaded'}), 400

if __name__ == '__main__':
    app.run()
