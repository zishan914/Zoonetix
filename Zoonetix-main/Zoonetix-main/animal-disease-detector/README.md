# Animal Disease Detection API

AI-based animal disease detection backend using FastAPI.

## Project Structure

- `app/main.py` - FastAPI application entry point
- `app/services/predict_service.py` - Image prediction logic
- `app/utils.py` - Image preprocessing utilities
- `app/schemas.py` - Response schema definitions
- `model/` - Place for saved AI model files
- `requirements.txt` - Python dependencies

## Setup

1. Create a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the API:

   ```powershell
   uvicorn app.main:app --reload
   ```

4. Open the frontend in browser:

   `http://127.0.0.1:8000`

5. Optional API docs:

   `http://127.0.0.1:8000/docs`

## Frontend

- A polished upload page is now available at `/`
- Upload a JPEG or PNG image and get an AI-based disease prediction

## AI Model Support

- Place a trained TensorFlow model at `model/my_mobilenet_model.keras`
- If TensorFlow is installed, the app will load your model and use CNN inference
- If the model file is missing, the app still runs with a fallback MobileNetV2 feature-extractor head

## API Endpoint

- `POST /predict`
  - form field: `file` (image/jpeg or image/png)
  - response: predicted disease, confidence, message

## Notes

- The prediction service loads `model/my_mobilenet_model.keras` by default.
- Save your trained model into `model/my_mobilenet_model.keras` and update the loading code if you use a different name.
