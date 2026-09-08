"""Notes API: HTTP layer on top of NoteStore."""

import os

from flask import Flask, jsonify, request

from notes import NoteNotFound, NoteStore

app = Flask(__name__)
store = NoteStore()


@app.get("/health")
def health():
    return {"status": "ok", "version": os.getenv("APP_VERSION", "dev")}


@app.get("/notes")
def list_notes():
    query = request.args.get("q")
    if query:
        return jsonify(store.search(query))
    return jsonify(store.all())


@app.post("/notes")
def create_note():
    data = request.get_json(silent=True) or {}
    try:
        note = store.add(data.get("title"), data.get("body", ""))
    except ValueError as exc:
        return {"error": str(exc)}, 400
    return note, 201


@app.get("/notes/<int:note_id>")
def get_note(note_id: int):
    try:
        return store.get(note_id)
    except NoteNotFound:
        return {"error": "not found"}, 404


@app.delete("/notes/<int:note_id>")
def delete_note(note_id: int):
    try:
        store.delete(note_id)
    except NoteNotFound:
        return {"error": "not found"}, 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
