# app/realtime.py
import time
import json
import queue
from threading import Lock

_event_q = queue.Queue()
_recent = []             # small ring buffer of recent events
_recent_lock = Lock()
MAX_RECENT = 500

def emit_event(evt: dict):
    """Push an event (dict) into the stream and recent buffer."""
    evt['_ts'] = time.time()
    _event_q.put(evt)
    with _recent_lock:
        _recent.append(evt)
        if len(_recent) > MAX_RECENT:
            _recent.pop(0)

def event_stream():
    """Generator for SSE — yields JSON events."""
    while True:
        try:
            evt = _event_q.get(timeout=1.0)
        except queue.Empty:
            # keep connection alive (comment out if you prefer)
            yield ":\n\n"
            continue
        data = json.dumps(evt, default=str)
        # SSE format
        yield f"data: {data}\n\n"

def get_recent():
    with _recent_lock:
        return list(_recent)
