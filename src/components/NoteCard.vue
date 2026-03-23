<template>
  <div
    class="note-card rounded-2xl p-4 relative overflow-hidden transition-all duration-300"
    :style="{
      backgroundColor: tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
      boxShadow: 'var(--shadow-md)',
    }"
    @click="$emit('view', note)"
  >
    <!-- Pin badge -->
    <span v-if="note.is_pinned" class="absolute top-3 right-3 text-base select-none">📌</span>

    <!-- Title -->
    <h3
      class="font-bold text-base mb-1 pr-6 leading-snug"
      :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
    >
      {{ note.title }}
    </h3>

    <!-- Preview -->
    <p
      class="text-sm leading-relaxed mb-3"
      :style="{ color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)' }"
    >
      {{ preview }}
    </p>

    <!-- Tags -->
    <div v-if="note.tags?.length" class="flex flex-wrap gap-1 mb-3">
      <span
        v-for="tag in note.tags"
        :key="tag"
        class="text-xs px-2 py-0.5 rounded-full"
        style="background: rgba(139,92,246,0.12); color: #8b5cf6;"
      >
        #{{ tag }}
      </span>
    </div>

    <!-- Footer row -->
    <div class="flex items-center justify-between">
      <span
        class="text-xs"
        :style="{ color: tg?.themeParams?.hint_color || 'var(--color-text-tertiary)' }"
      >
        {{ formattedDate }}
      </span>

      <!-- Action buttons -->
      <div class="flex gap-2" @click.stop>
        <button
          class="action-btn"
          :title="note.is_pinned ? 'Unpin' : 'Pin'"
          @click="$emit('pin', note.id)"
        >
          {{ note.is_pinned ? '📌' : '🔖' }}
        </button>
        <button class="action-btn" title="Delete" @click="$emit('delete', note.id)">
          🗑
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const tg = window.Telegram?.WebApp

const props = defineProps({
  note: { type: Object, required: true },
})

defineEmits(['view', 'pin', 'delete'])

const preview = computed(() => {
  const c = props.note.content ?? ''
  return c.length > 100 ? c.slice(0, 100) + '…' : c
})

const formattedDate = computed(() => {
  const d = props.note.created_at
  if (!d) return ''
  return new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
})
</script>

<style scoped>
.note-card {
  cursor: pointer;
}
.note-card:hover {
  transform: translateY(-2px);
}
.action-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  transition: background 150ms;
}
.action-btn:hover {
  background: rgba(0,0,0,0.06);
}
</style>
