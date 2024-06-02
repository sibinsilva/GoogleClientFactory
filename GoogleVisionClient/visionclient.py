import base64
from google.cloud import vision_v1

# Initialize the Vision API client
client = vision_v1.ImageAnnotatorClient()

def detect(request):
    # Ensure the request contains JSON payload
    request_json = request.get_json(silent=True)
    if not request_json:
        return {'error': 'Invalid request, expecting JSON payload'}, 400

    # Ensure necessary fields are present in the JSON payload
    if 'image_bytes' not in request_json or 'feature' not in request_json:
        return {'error': 'Missing "image_bytes" or "feature" field'}, 400

    try:
        image_bytes = base64.b64decode(request_json['image_bytes'])
        image = vision_v1.Image(content=image_bytes)
    except ValueError as e:
        return {'error': str(e)}, 400

    feature = request_json['feature']
    if feature == 'text_detection':
        response = client.text_detection(image=image)
        texts = [text.description for text in response.text_annotations]
        return {'detected_texts': texts}, 200
    elif feature == 'label_detection':
        response = client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        return {'label_annotations': labels}, 200
    elif feature == 'face_detection':
        response = client.face_detection(image=image)
        faces = [{'confidence': face.detection_confidence} for face in response.face_annotations]
        return {'face_annotations': faces}, 200
    elif feature == 'landmark_detection':
        response = client.landmark_detection(image=image)
        landmarks = [landmark.description for landmark in response.landmark_annotations]
        return {'landmark_annotations': landmarks}, 200
    elif feature == 'logo_detection':
        response = client.logo_detection(image=image)
        logos = [logo.description for logo in response.logo_annotations]
        return {'logo_annotations': logos}, 200
    elif feature == 'object_localization':
        response = client.object_localization(image=image)
        objects = [obj.name for obj in response.localized_object_annotations]
        return {'localized_object_annotations': objects}, 200
    elif feature == 'image_properties':
        response = client.image_properties(image=image)
        colors = [{'color': color.color, 'score': color.score} for color in response.image_properties_annotation.dominant_colors.colors]
        return {'image_properties_annotation': colors}, 200
    elif feature == 'safe_search_detection':
        response = client.safe_search_detection(image=image)
        safe_search = {
            'adult': response.safe_search_annotation.adult,
            'spoof': response.safe_search_annotation.spoof,
            'medical': response.safe_search_annotation.medical,
            'violence': response.safe_search_annotation.violence,
            'racy': response.safe_search_annotation.racy,
        }
        return {'safe_search_annotation': safe_search}, 200
    elif feature == 'web_detection':
        response = client.web_detection(image=image)
        web_entities = [entity.description for entity in response.web_detection.web_entities]
        return {'web_detection': web_entities}, 200
    else:
        return {'error': 'Unsupported feature'}, 400
