from flask import Flask, request, jsonify
from pytubefix import YouTube
import subprocess
import json

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

# Endpoint to get the streaming URI
@app.route('/streaming-uri', methods=['POST'])
def get_streaming_uri():
    try:
        data = request.get_json()
        video_url = data.get("url")
        po_token = data.get("poToken")  # Accept the PoToken from the request body

        if not video_url or not po_token:
            return jsonify({"error": "You must provide both a YouTube video URL and PoToken"}), 400

        # Use the PoToken while initializing YouTube
        yt = YouTube(video_url, use_po_token=True, token=po_token)
        stream = yt.streams.get_highest_resolution()

        return jsonify({"streaming_uri": stream.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
