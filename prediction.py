import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best_model.pkl")
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "..", "models", "preprocessor.pkl")

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)


def predict_churn(input_data):

    input_df = pd.DataFrame([input_data])

    input_processed = preprocessor.transform(input_df)

    prediction = model.predict(input_processed)[0]

    probability = model.predict_proba(input_processed)[0][1]

    return prediction, probability