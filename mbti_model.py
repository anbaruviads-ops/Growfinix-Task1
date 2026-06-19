import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "models/rf_model.pkl"
VEC_PATH = "models/vectorizer.pkl"
ENC_PATH = "models/encoder.pkl"


def train_model():

    df = pd.read_csv("data/mbti.csv")

    X_text = df["posts"]
    y_text = df["type"]

    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

    X = vectorizer.fit_transform(X_text)

    encoder = LabelEncoder()

    y = encoder.fit_transform(y_text)

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VEC_PATH)
    joblib.dump(encoder, ENC_PATH)

    print("MBTI model trained successfully")


def predict_mbti_ml(text):

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)
    encoder = joblib.load(ENC_PATH)

    X = vectorizer.transform([text])

    prediction = model.predict(X)

    prob = model.predict_proba(X)

    confidence = max(prob[0]) * 100

    mbti = encoder.inverse_transform(
        prediction
    )[0]

    return mbti, confidence


def predict_mbti_quiz(
    q1,
    q2,
    q3,
    q4,
    q5
):

    score_i = 0
    score_e = 0

    score_n = 0
    score_s = 0

    score_t = 0
    score_f = 0

    score_j = 0
    score_p = 0

    if q1 == "Working Alone":
        score_i += 1
    else:
        score_e += 1

    if q4 == "Deep Thinking":
        score_i += 1
    else:
        score_e += 1

    if q5 == "Ideas":
        score_n += 1
    else:
        score_s += 1

    if q2 == "Logic":
        score_t += 1
    else:
        score_f += 1

    if q3 == "Planner":
        score_j += 1
    else:
        score_p += 1

    mbti = ""

    mbti += "I" if score_i >= score_e else "E"
    mbti += "N" if score_n >= score_s else "S"
    mbti += "T" if score_t >= score_f else "F"
    mbti += "J" if score_j >= score_p else "P"

    return mbti