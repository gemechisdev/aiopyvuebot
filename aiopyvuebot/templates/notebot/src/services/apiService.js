/**
 * apiService.js
 * Communicates with the FastAPI backend.
 * Attaches Telegram initData to every request for server-side auth.
 */

import telegramService from "./telegramService.js";

const BASE = "/api";

/** Build default headers, injecting the Telegram auth token. */
function headers() {
  const init = telegramService.initData;
  return {
    "Content-Type": "application/json",
    Accept: "application/json",
    ...(init ? { Authorization: `Telegram ${init}` } : {}),
  };
}

async function handleResponse(res) {
  const ct = res.headers.get("content-type") ?? "";
  if (!ct.includes("application/json")) {
    throw new Error(`Unexpected response type: ${ct}`);
  }
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data?.detail ?? `HTTP ${res.status}`);
  }
  return data;
}

const api = {
  // ── Notes ──────────────────────────────────────────────────────────────────

  async getNotes({ limit = 20, skip = 0, q = "" } = {}) {
    const params = new URLSearchParams({ limit, skip });
    if (q) params.set("q", q);
    const res = await fetch(`${BASE}/notes/?${params}`, { headers: headers() });
    return handleResponse(res);
  },

  async getNote(id) {
    const res = await fetch(`${BASE}/notes/${id}`, { headers: headers() });
    return handleResponse(res);
  },

  async createNote({ title, content, tags = [] }) {
    const res = await fetch(`${BASE}/notes/`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ title, content, tags }),
    });
    return handleResponse(res);
  },

  async updateNote(id, updates) {
    const res = await fetch(`${BASE}/notes/${id}`, {
      method: "PUT",
      headers: headers(),
      body: JSON.stringify(updates),
    });
    return handleResponse(res);
  },

  async deleteNote(id) {
    const res = await fetch(`${BASE}/notes/${id}`, {
      method: "DELETE",
      headers: headers(),
    });
    if (res.status === 204) return true;
    return handleResponse(res);
  },

  async pinNote(id) {
    const res = await fetch(`${BASE}/notes/${id}/pin`, {
      method: "POST",
      headers: headers(),
    });
    return handleResponse(res);
  },
};

export default api;
