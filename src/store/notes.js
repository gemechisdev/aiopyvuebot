/**
 * notes.js  — Vue 3 composable that wraps all note state + API calls.
 * Module-level singleton: all calls to useNoteStore() share the same state.
 * Usage:  const store = useNoteStore()
 */

import { ref, computed, reactive } from "vue";
import api from "../services/apiService.js";

// ── Module-level singleton state ─────────────────────────────────────────────
// Declared outside useNoteStore() so every call returns the same refs.

const notes = ref([]);
const total = ref(0);
const isLoading = ref(false);
const isSaving = ref(false);
const error = ref(null);
const loadFailed = ref(false);

// ── derived ──────────────────────────────────────────────────────────────────

const pinnedNotes = computed(() => notes.value.filter((n) => n.is_pinned));
const unpinnedNotes = computed(() => notes.value.filter((n) => !n.is_pinned));

// ── helpers ───────────────────────────────────────────────────────────────────

function setError(msg) {
  error.value = msg;
  setTimeout(() => (error.value = null), 4000);
}

// ── actions ───────────────────────────────────────────────────────────────────

async function loadNotes(opts = {}) {
  isLoading.value = true;
  error.value = null;
  try {
    const res = await api.getNotes(opts);
    notes.value = res.notes ?? [];
    total.value = res.total ?? notes.value.length;
    loadFailed.value = false;
  } catch (e) {
    loadFailed.value = true;
    setError("Failed to load notes: " + e.message);
  } finally {
    isLoading.value = false;
  }
}

async function searchNotes(query) {
  return loadNotes({ q: query });
}

async function addNote({ title, content, tags }) {
  isSaving.value = true;
  error.value = null;
  try {
    const note = await api.createNote({ title, content, tags });
    notes.value.unshift(note);
    total.value += 1;
    return note;
  } catch (e) {
    setError("Failed to save note: " + e.message);
    return null;
  } finally {
    isSaving.value = false;
  }
}

async function updateNote(id, updates) {
  try {
    const updated = await api.updateNote(id, updates);
    const idx = notes.value.findIndex((n) => n.id === id);
    if (idx !== -1) notes.value[idx] = updated;
    return updated;
  } catch (e) {
    setError("Failed to update note: " + e.message);
    return null;
  }
}

async function deleteNote(id) {
  try {
    await api.deleteNote(id);
    notes.value = notes.value.filter((n) => n.id !== id);
    total.value = Math.max(0, total.value - 1);
    return true;
  } catch (e) {
    setError("Failed to delete note: " + e.message);
    return false;
  }
}

async function togglePin(id) {
  try {
    const updated = await api.pinNote(id);
    const idx = notes.value.findIndex((n) => n.id === id);
    if (idx !== -1) notes.value[idx] = updated;
    return updated;
  } catch (e) {
    setError("Failed to pin note: " + e.message);
    return null;
  }
}

export function useNoteStore() {
  // reactive() wraps the plain object so that nested refs are auto-unwrapped
  // in templates — without this, `store.isLoading` evaluates to a truthy Ref
  // object instead of the actual boolean, keeping the loading spinner forever.
  return reactive({
    notes,
    total,
    isLoading,
    isSaving,
    loadFailed,
    error,
    pinnedNotes,
    unpinnedNotes,
    loadNotes,
    searchNotes,
    addNote,
    updateNote,
    deleteNote,
    togglePin,
  });
}
