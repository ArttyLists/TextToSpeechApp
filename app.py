from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form['text']
    if text:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_file = "static/speech.mp3"
        tts.save(audio_file)
        return send_file(audio_file, as_attachment=True)
    return "Error: No text provided"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))

