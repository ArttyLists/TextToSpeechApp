from flask import Flask, render_template, request, redirect, url_for, flash
from gtts import gTTS
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Temporary storage for the converted text and the audio file path
converted_text = None
audio_file = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    global converted_text, audio_file
    text = request.form.get('text')
    
    if text:
        try:
            # Ensure 'static' directory exists
            static_folder = os.path.join(app.root_path, 'static')
            if not os.path.exists(static_folder):
                os.makedirs(static_folder)

            converted_text = text
            tts = gTTS(text=text, lang='en', slow=False)
            audio_file = os.path.join(static_folder, "speech.mp3")
            tts.save(audio_file)
            flash("Conversion successful! You can now download the audio.")
        except Exception as e:
            flash(f"Error during conversion: {str(e)}")
    else:
        flash("Error: No text provided")

    return redirect(url_for('index'))

@app.route('/download')
def download_audio():
    global audio_file
    if audio_file:
        return redirect(f'/static/speech.mp3')
    else:
        flash("No audio file to download!")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=True)
