from flask import Flask, request, jsonify
import speech_recognition as sr
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set up a path to store uploaded files temporarily
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def recognize_speech_from_audio(audio):
    """Convert audio to text using Google's Speech Recognition API"""
    recognizer = sr.Recognizer()
    response = {"success": True, "error": None, "transcription": None}

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """Handle microphone recording and file uploads"""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part in the request"})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"})

    # Save the uploaded file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    recognizer = sr.Recognizer()

    # Recognize the speech from the file
    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)

    result = recognize_speech_from_audio(audio)

    # Remove the uploaded file after processing
    os.remove(filepath)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
