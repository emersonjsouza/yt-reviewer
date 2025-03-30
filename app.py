from urllib.parse import parse_qs, urlparse

from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def extract_video_id(url):
    try:
        parsed = urlparse(url)
        if parsed.hostname == "youtu.be":
            return parsed.path[1:]
        elif parsed.hostname in ("www.youtube.com", "youtube.com"):
            return parse_qs(parsed.query).get("v", [None])[0]
    except Exception:
        pass
    return None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get-transcript', methods=['POST'])
def get_transcript():
    url = request.form.get("url", "")
    video_id = extract_video_id(url)
    error = ''
    transcript_text = ''

    if not video_id:
        error = "Invalid YouTube URL."
    else:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'pt'])
            lines = [f"[{round(entry['start'], 2)}s] {entry['text']}" for entry in transcript]
            transcript_text = "\n".join(lines)
        except Exception as e:
            error = f"Could not fetch transcript: {str(e)}"

    return render_template("transcript.html", transcript=transcript_text, error=error)


if __name__  == '__main__':
    app.run(debug=True)
