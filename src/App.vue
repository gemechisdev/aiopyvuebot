<template>
  <div class="min-h-screen pb-24 relative" :class="{ 'dark-theme': isDark }">
    <!-- Subtle background pattern -->
    <div class="fixed inset-0 pattern-dots pointer-events-none opacity-5" />

    <div class="max-w-lg mx-auto px-4 pt-4">

      <!-- Header -->
      <header class="text-center mb-5">
        <h1
          class="text-2xl font-bold mb-1"
          :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
        >
          📒 Note Manager
        </h1>
        <p
          class="text-sm"
          :style="{ color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)' }"
        >
          Your personal Telegram notes
        </p>
      </header>

      <!-- User info -->
      <UserInfo :user="user" :note-count="store.total" />

      <!-- Search bar -->
      <div class="relative mb-4">
        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-base opacity-50">🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search notes…"
          class="w-full pl-9 pr-4 py-2.5 rounded-xl text-sm border outline-none"
          :style="{
            backgroundColor: tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
            color: tg?.themeParams?.text_color || 'var(--color-text)',
            borderColor: 'var(--color-border)',
          }"
          @input="onSearch"
        />
      </div>

      <!-- Error banner -->
      <transition name="fade">
        <div
          v-if="store.error"
          class="mb-4 px-4 py-3 rounded-xl text-sm font-medium"
          style="background:#fee2e2; color:#b91c1c;"
        >
          ⚠️ {{ store.error }}
        </div>
      </transition>

      <!-- Loading spinner -->
      <div v-if="store.isLoading && !store.notes.length" class="flex justify-center py-16">
        <div class="w-10 h-10 rounded-full animate-spin"
          style="border:3px solid transparent; border-top-color:#8b5cf6; border-right-color:#ec4899;" />
      </div>

      <!-- Notes list -->
      <NoteList
        v-else
        :notes="store.notes"
        @view="openNote"
        @pin="togglePin"
        @delete="confirmDelete"
      />
    </div>

    <!-- Note detail overlay -->
    <transition name="slide-up">
      <div
        v-if="activeNote"
        class="fixed inset-0 z-40 flex items-end justify-center"
        style="background:rgba(0,0,0,0.4);"
        @click.self="activeNote = null"
      >
        <div
          class="w-full max-w-lg rounded-t-3xl p-5 pb-10 max-h-[85vh] overflow-y-auto"
          :style="{ backgroundColor: tg?.themeParams?.bg_color || 'var(--color-bg)' }"
        >
          <div class="w-12 h-1 rounded-full mx-auto mb-4" style="background:#d1d5db;" />
          <div class="flex items-start justify-between gap-2 mb-3">
            <h2
              class="text-lg font-bold flex-1"
              :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
            >
              {{ activeNote.is_pinned ? '📌' : '��' }} {{ activeNote.title }}
            </h2>
            <button class="text-xl" @click="activeNote = null">✕</button>
          </div>
          <p
            class="text-sm leading-relaxed whitespace-pre-wrap mb-4"
            :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
          >{{ activeNote.content }}</p>
          <div v-if="activeNote.tags?.length" class="flex flex-wrap gap-1 mb-4">
            <span
              v-for="t in activeNote.tags" :key="t"
              class="text-xs px-2 py-0.5 rounded-full"
              style="background:rgba(139,92,246,0.12);color:#8b5cf6;"
            >#{{ t }}</span>
          </div>
          <div class="flex gap-3">
            <button
              class="flex-1 py-2.5 rounded-xl text-sm font-medium border"
              :style="{ borderColor:'var(--color-border)', color: tg?.themeParams?.text_color || 'var(--color-text)' }"
              @click="togglePin(activeNote.id)"
            >
              {{ activeNote.is_pinned ? 'Unpin ��' : 'Pin 🔖' }}
            </button>
            <button
              class="flex-1 py-2.5 rounded-xl text-sm font-semibold text-white"
              style="background:#ef4444;"
              @click="confirmDelete(activeNote.id)"
            >🗑 Delete</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Note form modal -->
    <NoteForm
      :visible="showForm"
      :is-saving="store.isLoading"
      @close="showForm = false"
      @save="saveNote"
    />

    <!-- FAB – Add note -->
    <button
      v-if="!showForm && !activeNote"
      class="fixed bottom-6 right-6 z-30 w-14 h-14 rounded-full shadow-xl flex items-center justify-center text-white text-2xl transition-transform hover:scale-110"
      style="background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);"
      @click="showForm = true"
    >+</button>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import telegramService from './services/telegramService.js'
import { useNoteStore } from './store/notes.js'
import UserInfo from './components/UserInfo.vue'
import NoteList from './components/NoteList.vue'
import NoteForm from './components/NoteForm.vue'

const tg = window.Telegram?.WebApp
const user = ref(telegramService.getUserData())
const store = useNoteStore()

const searchQuery = ref('')
const showForm = ref(false)
const activeNote = ref(null)
const isDark = ref(false)

// ── search debounce ────────────────────────────────────────────────────────
let searchTimer = null
function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    if (searchQuery.value.trim()) {
      store.searchNotes(searchQuery.value.trim())
    } else {
      store.loadNotes()
    }
  }, 350)
}

// ── actions ────────────────────────────────────────────────────────────────
function openNote(note) {
  activeNote.value = note
}

async function saveNote(data) {
  const created = await store.addNote(data)
  if (created) showForm.value = false
}

async function togglePin(id) {
  const updated = await store.togglePin(id)
  if (updated && activeNote.value?.id === id) activeNote.value = updated
}

async function confirmDelete(id) {
  if (!confirm('Delete this note?')) return
  await store.deleteNote(id)
  if (activeNote.value?.id === id) activeNote.value = null
}

// ── lifecycle ──────────────────────────────────────────────────────────────
onMounted(() => {
  telegramService.init()
  store.loadNotes()

  // Telegram Back Button
  if (telegramService.isInTelegram) {
    const BOT_LINK = import.meta.env.VITE_TELEGRAM_BOT_LINK
    if (BOT_LINK) {
      telegramService.showMainButton('Back to Bot', () => {
        telegramService.openLink(BOT_LINK)
        telegramService.close()
      })
    }
  }

  // Dark theme detection
  if (tg?.themeParams?.bg_color) {
    const hex = tg.themeParams.bg_color.replace('#', '')
    const r = parseInt(hex.slice(0, 2), 16)
    const g = parseInt(hex.slice(2, 4), 16)
    const b = parseInt(hex.slice(4, 6), 16)
    isDark.value = (0.299 * r + 0.587 * g + 0.114 * b) / 255 < 0.5
  }
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 200ms; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 250ms, opacity 250ms; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(60px); opacity: 0; }
</style>
