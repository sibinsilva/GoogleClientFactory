import base64
from google.cloud import speech_v1p1beta1 as speech

def speech_to_text(request):
    # Get the request data
    request_json = request.get_json()
    if not request_json:
        return 'No JSON data provided in request.', 400

    if 'audio_content' not in request_json:
        return 'No audio content provided in request.', 400

    audio_content = request_json['audio_content']
    language_code = request_json.get('language_code', 'en-US')

    try:
        # Decode the base64 audio content
        audio = speech.RecognitionAudio(content=base64.b64decode(audio_content))

        client = speech.SpeechClient()

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=language_code
        )

        response = client.recognize(config=config, audio=audio)

        transcripts = []
        for result in response.results:
            transcripts.append(result.alternatives[0].transcript)

        return {'transcripts': transcripts}
    
    except Exception as e:
        return f'An error occurred: {str(e)}', 500
