# app/app.py
from flask import Flask, Response, request, jsonify, render_template
from dateutil import tz, parser
from realtime import event_stream, emit_event, get_recent
import joblib, os, json, time

app = Flask(__name__, template_folder='templates', static_folder='static')

# load your model as you already do — adjust path if needed
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'model.pkl')
VEC_PATH   = os.path.join(os.path.dirname(__file__), '..', 'model', 'vector.pkl')

model = None
vectorizer = None
try:
    data = joblib.load(MODEL_PATH)
    # if you saved differently, adapt:
    # model = data.get('model') ; vectorizer = data.get('vectorizer')
    # fallback if model.pkl is the model:
    model = data if hasattr(data, "predict") else None
except Exception:
    model = None

try:
    vec_data = joblib.load(VEC_PATH)
    vectorizer = vec_data if hasattr(vec_data, "transform") else None
except Exception:
    vectorizer = None

# load MITRE mapping (simple JSON mapping intent -> tactics)
MITRE_MAP_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'mitre_map.json')
if os.path.exists(MITRE_MAP_PATH):
    with open(MITRE_MAP_PATH) as f:
        MITRE_MAP = json.load(f)
else:
    MITRE_MAP = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/api/recent', methods=['GET'])
def api_recent():
    return jsonify(get_recent())

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    payload = request.json or {}
    text = payload.get('text') or payload.get('input') or ''
    src_ip = payload.get('src_ip', 'unknown')
    # model inference
    pred = "unknown"
    cat = "uncategorized"
    score = 0.0
    if model is not None:
        try:
            features = vectorizer.transform([text]) if vectorizer is not None else [text]
            pred = model.predict([features])[0] if hasattr(model, "predict") else "unknown"
            # if model provides predict_proba:
            if hasattr(model, "predict_proba"):
                score = float(max(model.predict_proba([features])[0]))
        except Exception as e:
            pred = "error"
    # MITRE mapping
    mitre = MITRE_MAP.get(pred, {})
    event = {
        "type": "analysis",
        "intent": pred,
        "text": text,
        "category": cat,
        "risk": score,
        "src_ip": src_ip,
        "mitre": mitre,
        "time": time.time()
    }
    emit_event(event)
    return jsonify(event)

@app.route('/api/mitre_lookup', methods=['POST'])
def api_mitre_lookup():
    body = request.json or {}
    intent = body.get('intent')
    return jsonify(MITRE_MAP.get(intent, {}))

# utility endpoint for honeypot to push events (if you want remote push)
@app.route('/api/push_event', methods=['POST'])
def api_push_event():
    evt = request.json or {}
    evt.setdefault('type', 'honeypot')
    evt.setdefault('time', time.time())
    emit_event(evt)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9900)
