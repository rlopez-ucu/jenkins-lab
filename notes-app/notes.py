"""In-memory note store. Pure Python, no framework, so it is easy to unit test."""


class NoteNotFound(Exception):
    pass


class NoteStore:
    def __init__(self):
        self._notes: dict[int, dict] = {}
        self._next_id = 1

    def add(self, title: str, body: str = "") -> dict:
        title = (title or "").strip()
        if not title:
            raise ValueError("title is required")
        note = {"id": self._next_id, "title": title, "body": body}
        self._notes[note["id"]] = note
        self._next_id += 1
        return note

    def get(self, note_id: int) -> dict:
        try:
            return self._notes[note_id]
        except KeyError:
            raise NoteNotFound(note_id) from None

    def all(self) -> list[dict]:
        return list(self._notes.values())

    def delete(self, note_id: int) -> None:
        if note_id not in self._notes:
            raise NoteNotFound(note_id)
        del self._notes[note_id]

    def search(self, text: str) -> list[dict]:
        text = text.lower()
        return [n for n in self._notes.values() if text in n["title"].lower() or text in n["body"].lower()]

    def clear(self) -> None:
        self._notes.clear()
        self._next_id = 1
