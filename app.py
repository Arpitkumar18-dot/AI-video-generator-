from flask import Flask, render_template, request, send_file
from gtts import gTTS
from moviepy.editor import *
import os, time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    video_ready = False

    if request.method == "POST":
        text = request.form["text"]

        os.makedirs("static", exist_ok=True)

        # text → voice
        tts = gTTS(text)
        audio_path = "static/voice.mp3"
        tts.save(audio_path)

        # simple image → video (temporary)
        clip = ImageClip("static/static.jpg").set_duration(5)
        audio = AudioFileClip(audio_path)
        final = clip.set_audio(audio)

        final.write_videofile(
            "static/output.mp4",
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        video_ready = True

    return render_template("index.html", video_ready=video_ready)

@app.route("/download")
def download():
    return send_file("static/output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
