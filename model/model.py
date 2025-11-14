import pickle
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VEC_PATH   = os.path.join(BASE_DIR, "vector.pkl")

model = None
vectorizer = None

def ensure_loaded():
    global model, vectorizer
    if model is None or vectorizer is None:
        load_model()

def load_model():
    global model, vectorizer
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VEC_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

def predict_intent(text: str):
    ensure_loaded()
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    return pred
