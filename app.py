# app.py
import os, sys, threading, time, webbrowser
from flask import Flask, render_template, jsonify, request, abort
import requests

API_BASE = os.getenv("STREAMS_API_BASE", "https://ppv.to")  # change me
API_URL = f"{API_BASE}/api/streams"
CACHE_TTL = 60  # seconds

BASE_PATH = getattr(sys, "_MEIPASS", os.path.abspath("."))
TEMPLATES = os.path.join(BASE_PATH, "templates")

app = Flask(__name__, template_folder=TEMPLATES)
_cache = {"at": 0, "payload": None}

def _open_browser_when_ready(url="http://127.0.0.1:5000/"):
    # give the server a moment to start, then open default browser
    def _opener():
        for _ in range(20):
            try:
                # quick ping; if it fails just retry shortly
                requests.get(url, timeout=0.3)
                break
            except Exception:
                time.sleep(0.2)
        try:
            webbrowser.open(url)
        except Exception:
            pass
    threading.Thread(target=_opener, daemon=True).start()

def _status(now, s):
    if s.get("always_live") == 1:
        return "live"
    start, end = s.get("starts_at"), s.get("ends_at")
    if not start or not end:
        return "unknown"
    if now < start: return "upcoming"
    if start <= now <= end: return "live"
    return "ended"

def get_streams_cached():
    now = int(time.time())
    if _cache["payload"] and now - _cache["at"] < CACHE_TTL:
        return _cache["payload"]
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()

    # Flatten categories → list of streams with category info and computed status
    flat = []
    for cat in data.get("streams", []):
        cat_name = cat.get("category")
        for s in cat.get("streams", []):
            s2 = {
                "id": s.get("id"),
                "name": s.get("name"),
                "tag": s.get("tag"),
                "poster": s.get("poster"),
                "uri_name": s.get("uri_name"),
                "starts_at": s.get("starts_at"),
                "ends_at": s.get("ends_at"),
                "always_live": s.get("always_live", 0),
                "allowpaststreams": s.get("allowpaststreams", 0),
                "category": cat_name,
                # NOTE: some providers include "iframe" directly; if present we keep it
                "iframe": s.get("iframe"),
            }
            s2["status"] = _status(now, s2)
            flat.append(s2)

    out = {
        "timestamp": data.get("timestamp"),
        "performance": data.get("performance"),
        "items": flat
    }
    _cache.update({"at": now, "payload": out})
    return out

@app.get("/")
def select_screen():
    return render_template("select.html")

@app.get("/api/streams")
def api_streams():
    # Optional server-side filters (simple, fast)
    q = (request.args.get("q") or "").lower().strip()
    status = request.args.get("status")  # live|upcoming|ended
    category = request.args.get("category")  # exact match
    data = get_streams_cached()
    items = data["items"]

    if q:
        items = [s for s in items if q in (s["name"] or "").lower() or q in (s["tag"] or "").lower() or q in (s["category"] or "").lower()]
    if status:
        items = [s for s in items if s["status"] == status]
    if category:
        items = [s for s in items if s["category"] == category]

    return jsonify({"timestamp": data["timestamp"], "count": len(items), "items": items})

@app.get("/watch")
def watch():
    ids_param = (request.args.get("ids") or "").strip()
    if not ids_param:
        abort(400, "Missing ids")
    try:
        wanted = [int(x) for x in ids_param.split(",") if x.strip().isdigit()]
    except ValueError:
        abort(400, "Bad ids")

    data = get_streams_cached()
    by_id = {s["id"]: s for s in data["items"]}
    items = [by_id[i] for i in wanted if i in by_id]

    if not items:
        abort(404, "No matching streams")

    return render_template("watch.html", streams=items)

if __name__ == "__main__":
    _open_browser_when_ready()
    # Don’t use debug=True in a packaged app
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=False)