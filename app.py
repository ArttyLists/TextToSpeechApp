from flask import Flask, render_template, request, redirect, url_for, flash
from gtts import gTTS
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html', audio_file=None)

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form.get('text')
    
    if text:
        try:
            # Ensure 'static' directory exists
            static_folder = os.path.join(app.root_path, 'static')
            if not os.path.exists(static_folder):
                os.makedirs(static_folder)

            tts = gTTS(text=text, lang='en', slow=False)
            audio_file = os.path.join('static', 'speech.mp3')  # Save relative path for front-end
            tts.save(os.path.join(app.root_path, audio_file))
            flash("Conversion successful! You can now download the audio.")
            return render_template('index.html', audio_file=audio_file)
        except Exception as e:
            flash(f"Error during conversion: {str(e)}")
            return render_template('index.html', audio_file=None)
    else:
        flash("Error: No text provided")
        return render_template('index.html', audio_file=None)

@app.route('/download')
def download_audio():
    audio_file = os.path.join('static', 'speech.mp3')
    if os.path.exists(audio_file):
        return redirect(f'/{audio_file}')
    else:
        flash("No audio file to download!")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=True)
