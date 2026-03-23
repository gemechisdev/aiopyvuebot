/**
 * notes.js  — Vue 3 composable that wraps all note state + API calls.
 * Usage:  const store = useNoteStore()
 */

import { ref, computed } from "vue";
import api from "../services/apiService.js";

export function useNoteStore() {
  const notes = ref([]);
  const total = ref(0);
  const isLoading = ref(false);
  const error = ref(null);
  const activeNote = ref(null);

  // ── derived ──────────────────────────────────────────────────────────────

  const pinnedNotes = computed(() => notes.value.filter((n) => n.is_pinned));
  const unpinnedNotes = computed(() => notes.value.filter((n) => !n.is_pinned));

  // ── helpers ──────────────────────────────────────────────────────────────

  function setError(msg) {
    error.value = msg;
    setTimeout(() => (error.value = null), 4000);
  }

  // ── actions ──────────────────────────────────────────────────────────────

  async function loadNotes(opts = {}) {
    isLoading.value = true;
    error.value = null;
    try {
      const res = await api.getNotes(opts);
      notes.value = res.notes ?? [];
      total.value = res.total ?? notes.value.length;
    } catch (e) {
      setError("Failed to load notes: " + e.message);
    } finally {
      isLoading.value = false;
    }
  }

  async function searchNotes(query) {
    return loadNotes({ q: query });
  }

  async function addNote({ title, content, tags }) {
    isLoading.value = true;
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
      isLoading.value = false;
    }
  }

  async function updateNote(id, updates) {
    try {
      const updated = await api.updateNote(id, updates);
      const idx = notes.value.findIndex((n) => n.id === id);
      if (idx !== -1) notes.value[idx] = updated;
      if (activeNote.value?.id === id) activeNote.value = updated;
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
      if (activeNote.value?.id === id) activeNote.value = null;
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
      if (activeNote.value?.id === id) activeNote.value = updated;
      return updated;
    } catch (e) {
      setError("Failed to pin note: " + e.message);
      return null;
    }
  }

  return {
    notes,
    total,
    isLoading,
    error,
    activeNote,
    pinnedNotes,
    unpinnedNotes,
    loadNotes,
    searchNotes,
    addNote,
    updateNote,
    deleteNote,
    togglePin,
  };
}
