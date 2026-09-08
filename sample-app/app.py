"""Libreria API: a tiny Flask service used as the sample project for the Jenkins class."""

import os

from flask import Flask, jsonify, request

app = Flask(__name__)

BOOKS: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok", "version": os.getenv("APP_VERSION", "dev")}


@app.get("/books")
def list_books():
    return jsonify(BOOKS)


@app.post("/books")
def add_book():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return {"error": "title is required"}, 400
    book = {
        "id": len(BOOKS) + 1,
        "title": title,
        "author": data.get("author", "unknown"),
    }
    BOOKS.append(book)
    return book, 201


@app.get("/books/<int:book_id>")
def get_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return {"error": "not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
