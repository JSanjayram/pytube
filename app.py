from flask import Flask, request, jsonify
from pytubefix import YouTube
import subprocess
import json
import os

app = Flask(__name__)

# Endpoint to generate the PoToken
@app.route('/generate-token', methods=['GET'])
def generate_token():
    try:
        # Call the youtube-po-token-generator CLI tool using subprocess
        result = subprocess.run(
            ["youtube-po-token-generator"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # Parse the output from the tool
        if result.returncode == 0:
            token_data = json.loads(result.stdout)
            return jsonify(token_data)  # Returns { "visitorData": "...", "poToken": "..." }
        else:
            return jsonify({"error": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import traceback

@app.route('/streaming-uri', methods=['POST'])
def get_streaming_uri():
    try:
        data = request.get_json()
        video_url = data.get("url")
        po_token = data.get("poToken")
        visitor_data = data.get("visitorData")  # Assuming you also want to receive visitorData

        if not video_url or not po_token or not visitor_data:
            return jsonify({"error": "You must provide a YouTube video URL, PoToken, and visitorData"}), 400

        # Debugging: Print received token and video URL
        print(f"Received video URL: {video_url}")
        print(f"Received PoToken: {po_token}")
        print(f"Received visitorData: {visitor_data}")

        # Initialize YouTube with PoToken and visitorData
        yt = YouTube(video_url, use_po_token=True)


        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        return jsonify({"streaming_uri": stream.url})
    except Exception as e:
        error_message = str(e)
        print("Error occurred:", error_message)
        traceback.print_exc()  # Print the full traceback
        return jsonify({"error": error_message}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
