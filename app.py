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

@app.route('/streaming-uri', methods=['GET'])
def get_streaming_uri():
    try:
        # Retrieve the parameters from the query string
        video_url = request.args.get("url")
        po_token = request.args.get("poToken")

        if not video_url or not po_token:
            return jsonify({"error": "You must provide both a YouTube video URL and PoToken"}), 400

        # Debug logging
        print(f"Processing video URL: {video_url}")
        print(f"Using PoToken: {po_token}")

        # Use the PoToken while initializing YouTube
        yt = YouTube(video_url, use_po_token=True, token=po_token)
        stream = yt.streams.get_highest_resolution()

        return jsonify({"streaming_uri": stream.url})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
