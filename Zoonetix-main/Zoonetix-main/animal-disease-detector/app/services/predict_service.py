import os
from typing import Optional
import numpy as np
from app.schemas import PredictionResponse
from app.utils import preprocess_image
from app.treatment_data import get_treatment

DISEASE_LABELS = [
    "Eye Infection",
    "Fungal Infection",
    "Mange in Dog",
    "Parvovirus in Dog",
    "Scabies in Cat",
    "Skin Allergy",
    "foot-and-mouth",
    "healthy",
    "lumpy",
]

# Only accept these animals
ACCEPTED_ANIMALS = ["dog", "cat", "cow"]
MODEL_FILENAME = "my_mobilenet_model.keras"
MODEL_FILEPATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "model", MODEL_FILENAME)
)

_model = None
_tf = None


def _try_import_tensorflow():
    global _tf
    if _tf is None:
        try:
            import tensorflow as tf
            _tf = tf
        except ImportError:
            _tf = False
    return _tf


def _load_model():
    global _model
    if _model is not None:
        return _model

    tf = _try_import_tensorflow()
    if not tf:
        return None

    if os.path.exists(MODEL_FILEPATH):
        _model = tf.keras.models.load_model(MODEL_FILEPATH)
        return _model

    return None


def _ensure_face_detector_model(model_dir: str):
    """Download OpenCV DNN face detector files if missing."""
    import urllib.request
    os.makedirs(model_dir, exist_ok=True)
    prototxt = os.path.join(model_dir, "deploy.prototxt")
    caffemodel = os.path.join(model_dir, "res10_300x300_ssd_iter_140000.caffemodel")
    if not os.path.exists(prototxt):
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
            prototxt,
        )
    if not os.path.exists(caffemodel):
        urllib.request.urlretrieve(
            "https://github.com/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel",
            caffemodel,
        )
    return prototxt, caffemodel


def _is_likely_human(image_bytes: bytes) -> bool:
    """Use OpenCV DNN face detector to reject human photos."""
    try:
        import cv2
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return False

        model_dir = os.path.join(os.path.dirname(__file__), "..", "..", "model", "face_detector")
        model_dir = os.path.abspath(model_dir)
        prototxt, caffemodel = _ensure_face_detector_model(model_dir)

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104.0, 177.0, 123.0], False, False)
        net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = float(detections[0, 0, i, 2])
            # Higher threshold to avoid false positives on dogs/cats - only detect clear human faces
            if confidence > 0.8:
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                face_area = (x2 - x1) * (y2 - y1)
                img_area = h * w
                # Only count significant face detections
                if face_area > img_area * 0.05:
                    return True
        return False
    except Exception:
        return False


def _get_animal_type(image_bytes: bytes) -> str:
    """Detect if the image is a dog, cat, cow, using image classification."""
    try:
        # Use MobileNet to classify the animal type
        tf = _try_import_tensorflow()
        if not tf:
            return "unknown"

        # Load MobileNet for animal classification (not the disease model)
        import urllib.request
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        from PIL import Image
        from io import BytesIO

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = Image.open(BytesIO(nparr)).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.asarray(img, dtype=np.float32)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Load MobileNet with ImageNet weights
        base_model = MobileNetV2(weights='imagenet', include_top=True, input_shape=(224, 224, 3))
        predictions = base_model.predict(img_array, verbose=0)

        # Use top-5 predictions to better handle unusual dog/cat appearances
        decode_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)
        top_preds = decode_predictions[0]
        labels = [pred[1].lower() for pred in top_preds]
        label_str = " ".join(labels)

        dog_keywords = [
            'dog', 'retriever', 'shepherd', 'terrier', 'hound', 'beagle', 'pug',
            'bulldog', 'spaniel', 'chihuahua', 'boxer', 'rottweiler', 'doberman'
        ]
        cat_keywords = [
            'cat', 'tabby', 'persian', 'siamese', 'egyptian_cat', 'maine_coon', 'tiger_cat'
        ]
        cow_keywords = ['cow', 'ox', 'bull', 'bullock', 'zebu', 'jersey', 'guernsey']
        human_keywords = [
            'person', 'human', 'man', 'woman', 'boy', 'girl'
        ]
        other_keywords = [
            'goat', 'sheep', 'ibex', 'horse', 'zebra', 'pony', 'bird', 'chicken',
            'duck', 'goose', 'rabbit', 'hare', 'bunny'
        ]

        if any(keyword in label_str for keyword in dog_keywords):
            return "dog"
        elif any(keyword in label_str for keyword in cat_keywords):
            return "cat"
        elif any(keyword in label_str for keyword in cow_keywords):
            return "cow"
        elif any(keyword in label_str for keyword in human_keywords):
            return "human"
        elif any(keyword in label_str for keyword in other_keywords):
            return "other"
        else:
            return "unknown"
    except Exception:
        return "unknown"


def predict_animal_disease(image_bytes: bytes) -> PredictionResponse:
    tf = _try_import_tensorflow()
    if not tf:
        raise RuntimeError(
            "TensorFlow is not installed. Install it with `pip install tensorflow` to use the model."
        )

    # First, check animal type using MobileNet so valid dog/cat/cow images are not accidentally rejected by the face detector.
    animal_type = _get_animal_type(image_bytes)

    if animal_type == "human":
        return PredictionResponse(
            disease="Human Detected",
            confidence=1.0,
            message="⚠️ Human detected! This model is designed for livestock (dog, cat, cow). Please upload an animal photo."
        )
    elif animal_type not in ACCEPTED_ANIMALS:
        # If MobileNet is unsure, use face detection only to catch clear human photos.
        if _is_likely_human(image_bytes):
            return PredictionResponse(
                disease="Human Detected",
                confidence=1.0,
                message="⚠️ Human detected! This model is designed for livestock (dog, cat, cow). Please upload an animal photo."
            )

        return PredictionResponse(
            disease="Unsupported Animal",
            confidence=1.0,
            message="⚠️ This app only supports disease detection for dogs, cats, and cows. Please upload a dog, cat, or cow photo only."
        )
    # For dog, cat, or cow - allow to pass through and do disease prediction

    # NOTE: If your Colab notebook used tf.keras.applications.mobilenet_v2.preprocess_input
    # during training, uncomment the next line and pass preprocess_fn=preprocess_fn below.
    # preprocess_fn = tf.keras.applications.mobilenet_v2.preprocess_input
    image = preprocess_image(image_bytes, target_size=(224, 224))
    model = _load_model()

    if model is None:
        raise RuntimeError(
            f"No trained TensorFlow model found at {MODEL_FILEPATH}. "
            "Place your trained .keras model in the model/ directory."
        )

    batch = np.expand_dims(image, axis=0)
    predictions = model.predict(batch, verbose=0)
    probs = predictions[0] if hasattr(predictions, 'ndim') and predictions.ndim == 2 else np.asarray(predictions).reshape(-1)
    class_id = int(np.argmax(probs))
    confidence = float(np.max(probs))

    # Check if confidence is too low - probably not a clear animal photo
    if confidence < 0.3:
        return PredictionResponse(
            disease="Unclear Image",
            confidence=confidence,
            message="⚠️ Could not detect a clear animal. Please upload a clear photo of a dog, cat, or cow for disease detection."
        )

    if class_id >= len(DISEASE_LABELS):
        raise RuntimeError(
            f"Model returned class index {class_id}, but only {len(DISEASE_LABELS)} labels are configured. "
            f"Model output shape may be {getattr(predictions, 'shape', 'unknown')}. "
            "Ensure the model was trained with the same classes and preprocessing as the app expects."
        )

    label = DISEASE_LABELS[class_id]
    message = (
        "AI-based prediction using MobileNet CNN model. "
        + (
            f"Loaded trained model from model/{MODEL_FILENAME}."
            if os.path.exists(MODEL_FILEPATH)
            else "Trained model not found; predictions may be unreliable."
        )
    )
    treatment_info = get_treatment(label)
    return PredictionResponse(disease=label, confidence=confidence, message=message, treatment=treatment_info)
