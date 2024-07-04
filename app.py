from flask import Flask, request, render_template, jsonify
from deep_translator import GoogleTranslator
from langdetect import DetectorFactory, detect_langs

# Initialize the detector factory
DetectorFactory.seed = 0

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.form['text']
        target_lang = request.form.get('target_lang', 'en')  # default target language is English
        source_lang = detect_langs(text)[0].lang
        
        if source_lang == target_lang:
            translated_text = text
        else:
            translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        
        return render_template('result.html', translated_text=translated_text)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message and HTTP status code 500 (Internal Server Error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
