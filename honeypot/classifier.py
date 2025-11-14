# e.g. honeypot/classifier.py (example)
import requests, time, json
# local push (best): import emit_event directly
from app.realtime import emit_event

def on_detect(intent, text, src_ip):
    evt = {
        "type": "honeypot",
        "intent": intent,
        "text": text,
        "src_ip": src_ip,
        "severity": "high" if intent=='brute' else "medium"
    }
    emit_event(evt)
