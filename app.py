from flask import Flask, request, jsonify
from pytubefix import YouTube

app = Flask(__name__)

@app.route('/streaming-uri', methods=['POST'])
def get_streaming_uri():
    try:
        # Get the YouTube URL from the request
        data = request.get_json()
        video_url = data.get("url")

        if not video_url:
            return jsonify({"error": "You must provide a YouTube video URL"}), 400

        # Process the YouTube video
        yt = YouTube(video_url,use_po_token=True)
        stream = yt.streams.get_highest_resolution()

        # Return the streaming URI
        return jsonify({"streaming_uri": stream.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
