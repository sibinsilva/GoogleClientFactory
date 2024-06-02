import os
from google.cloud import texttospeech

def text_to_speech(request):
    try:
        # Check if request contains text
        request_json = request.get_json(silent=True)
        if request_json and 'text' in request_json:
            text = request_json['text']
        else:
            return 'Error: No text provided in request.', 400
        
        # Check if request contains language code, default to 'en-US'
        language_code = request_json.get('language_code', 'en-US')

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code and the ssml voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        audio_content = response.audio_content

        return audio_content, 200, {'Content-Type': 'audio/wav'}

    except Exception as e:
        return f'Error: {e}', 500
