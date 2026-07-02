# Model Folder

Place your trained TensorFlow model file here.

Example path:
- `model/my_mobilenet_model.keras`

The API will automatically load `model/my_mobilenet_model.keras` if TensorFlow is installed.

If the model file is not present, the app will return a fallback response instead of real disease inference.

This project is an image classification pipeline, so it uses a transfer learning classifier rather than an object detector such as YOLOv8.

To train a better classifier, use the training script added here and save the trained model as `animal_disease_model.keras`.

## Recommended dataset structure

Create a directory with one subfolder per class, matching the model labels exactly:

```
<dataset_root>/
  Healthy/
  Mastitis/
  Foot-and-mouth disease/
  Pneumonia/
  Skin infection/
```

Each subfolder should contain JPG or PNG images for that label.

## Training

Install TensorFlow and run the trainer:

```bash
pip install tensorflow
python model/train_model.py --data-dir path/to/your/dataset --output model/animal_disease_model.keras --epochs 8
```

After training, restart the FastAPI server and upload images again. The app will then use the real model for predictions.
