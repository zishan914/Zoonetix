from io import BytesIO
from PIL import Image
import numpy as np
from typing import Optional, Callable


def preprocess_image(
    image_bytes: bytes,
    target_size=(224, 224),
    preprocess_fn: Optional[Callable[[np.ndarray], np.ndarray]] = None,
) -> np.ndarray:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize(target_size)
    array = np.asarray(image, dtype=np.float32)
    if preprocess_fn is not None:
        array = preprocess_fn(array)
    else:
        array = array / 255.0
    return array
