<template>
  <div class="space-y-3">
    <!-- Empty state -->
    <div
      v-if="!notes.length"
      class="text-center py-16 px-4"
    >
      <div class="text-5xl mb-4">📭</div>
      <p
        class="font-semibold text-lg mb-1"
        :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
      >
        No notes yet
      </p>
      <p
        class="text-sm"
        :style="{ color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)' }"
      >
        Tap <b>+ New Note</b> below to get started.
      </p>
    </div>

    <!-- Note cards -->
    <NoteCard
      v-for="note in notes"
      :key="note.id"
      :note="note"
      @view="$emit('view', note)"
      @pin="$emit('pin', $event)"
      @delete="$emit('delete', $event)"
    />
  </div>
</template>

<script setup>
import NoteCard from './NoteCard.vue'

const tg = window.Telegram?.WebApp

defineProps({
  notes: { type: Array, required: true },
})

defineEmits(['view', 'pin', 'delete'])
</script>
