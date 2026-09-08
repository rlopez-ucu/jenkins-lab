"""Unit tests for the NoteStore, with no HTTP involved."""

import pytest

from notes import NoteNotFound, NoteStore


@pytest.fixture
def store():
    return NoteStore()


def test_add_returns_note_with_incremental_id(store):
    first = store.add("Comprar leche")
    second = store.add("Llamar al banco", "antes de las 15")
    assert first["id"] == 1
    assert second["id"] == 2
    assert second["body"] == "antes de las 15"


def test_add_strips_title(store):
    note = store.add("   con espacios   ")
    assert note["title"] == "con espacios"


@pytest.mark.parametrize("title", ["", "   ", None])
def test_add_rejects_empty_title(store, title):
    with pytest.raises(ValueError):
        store.add(title)


def test_get_existing(store):
    note = store.add("Una nota")
    assert store.get(note["id"]) == note


def test_get_missing_raises(store):
    with pytest.raises(NoteNotFound):
        store.get(42)


def test_all_returns_notes_in_insertion_order(store):
    store.add("a")
    store.add("b")
    store.add("c")
    assert [n["title"] for n in store.all()] == ["a", "b", "c"]


def test_delete_removes_note(store):
    note = store.add("temporal")
    store.delete(note["id"])
    assert store.all() == []


def test_delete_missing_raises(store):
    with pytest.raises(NoteNotFound):
        store.delete(99)


def test_search_matches_title_and_body_case_insensitive(store):
    store.add("Jenkins", "clase de devops")
    store.add("Compras", "leche y pan")
    store.add("Docker", "IMAGENES y contenedores")
    assert [n["title"] for n in store.search("jenkins")] == ["Jenkins"]
    assert [n["title"] for n in store.search("LECHE")] == ["Compras"]
    assert [n["title"] for n in store.search("e")] == ["Jenkins", "Compras", "Docker"]
    assert store.search("nada") == []


def test_clear_resets_ids(store):
    store.add("x")
    store.clear()
    assert store.add("y")["id"] == 1
