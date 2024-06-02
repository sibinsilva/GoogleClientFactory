import json
from google.cloud import translate_v2 as translate

def translate_text(request):
    request_json = request.get_json()
    
    try:
        # Check if the required fields are present in the request
        if not request_json or 'text' not in request_json:
            return 'Missing required field: "text"', 400
        
        # Extract text and target language from the request
        text = request_json['text']
        target_language = request_json.get('target_language', 'en')  # Default to English if not provided
        
        # Initialize the translation client
        client = translate.Client()
        
        # Translate the text
        translation = client.translate(text, target_language=target_language)
        
        # Return the translated text
        return json.dumps({'translated_text': translation['translatedText']}), 200, {'Content-Type': 'application/json'}
    
    except Exception as e:
        return str(e), 500
