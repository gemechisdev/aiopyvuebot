<template>
  <!-- Modal backdrop -->
  <transition name="fade">
    <div
      v-if="visible"
      class="fixed inset-0 z-50 flex items-end justify-center"
      style="background: rgba(0,0,0,0.45);"
      @click.self="$emit('close')"
    >
      <!-- Sheet -->
      <div
        class="w-full max-w-lg rounded-t-3xl p-5 pb-8 space-y-4"
        :style="{
          backgroundColor: tg?.themeParams?.bg_color || 'var(--color-bg)',
          boxShadow: '0 -8px 30px rgba(0,0,0,0.15)',
        }"
      >
        <!-- Handle bar -->
        <div class="w-12 h-1 rounded-full mx-auto" style="background:#d1d5db;" />

        <h2
          class="text-lg font-bold text-center"
          :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
        >
          📝 New Note
        </h2>

        <!-- Title -->
        <div>
          <label class="block text-sm font-medium mb-1" :style="labelStyle">Title</label>
          <input
            v-model="form.title"
            type="text"
            placeholder="My note title…"
            class="w-full rounded-xl px-4 py-2.5 text-sm border outline-none"
            :style="inputStyle"
            @keydown.enter.prevent="focusContent"
          />
        </div>

        <!-- Content -->
        <div>
          <label class="block text-sm font-medium mb-1" :style="labelStyle">Content</label>
          <textarea
            ref="contentRef"
            v-model="form.content"
            placeholder="Write your note here…"
            rows="5"
            class="w-full rounded-xl px-4 py-2.5 text-sm border outline-none resize-none"
            :style="inputStyle"
          />
        </div>

        <!-- Tags -->
        <div>
          <label class="block text-sm font-medium mb-1" :style="labelStyle">
            Tags <span class="font-normal opacity-60">(comma-separated)</span>
          </label>
          <input
            v-model="tagsRaw"
            type="text"
            placeholder="work, ideas, todo"
            class="w-full rounded-xl px-4 py-2.5 text-sm border outline-none"
            :style="inputStyle"
          />
        </div>

        <!-- Error -->
        <p v-if="validationError" class="text-xs text-red-500 -mt-1">{{ validationError }}</p>

        <!-- Actions -->
        <div class="flex gap-3 pt-1">
          <button
            class="flex-1 py-3 rounded-xl font-medium text-sm border transition-all"
            :style="cancelStyle"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            class="flex-1 py-3 rounded-xl font-semibold text-sm text-white transition-all hover:opacity-90"
            style="background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);"
            :disabled="isSaving"
            @click="submit"
          >
            {{ isSaving ? 'Saving…' : 'Save Note' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const tg = window.Telegram?.WebApp

const props = defineProps({
  visible: { type: Boolean, default: false },
  isSaving: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'save'])

const form = ref({ title: '', content: '' })
const tagsRaw = ref('')
const validationError = ref('')
const contentRef = ref(null)

// Reset when shown
watch(() => props.visible, (v) => {
  if (v) {
    form.value = { title: '', content: '' }
    tagsRaw.value = ''
    validationError.value = ''
  }
})

function focusContent() {
  nextTick(() => contentRef.value?.focus())
}

function submit() {
  validationError.value = ''
  if (!form.value.title.trim()) {
    validationError.value = 'Title is required.'
    return
  }
  if (!form.value.content.trim()) {
    validationError.value = 'Content is required.'
    return
  }
  const tags = tagsRaw.value
    .split(',')
    .map((t) => t.trim().toLowerCase())
    .filter(Boolean)
  emit('save', { ...form.value, tags })
}

// ── Styles ────────────────────────────────────────────────────────────────────
const labelStyle = computed(() => ({
  color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
}))

const inputStyle = computed(() => ({
  backgroundColor: tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
  color: tg?.themeParams?.text_color || 'var(--color-text)',
  borderColor: 'var(--color-border)',
}))

const cancelStyle = computed(() => ({
  borderColor: 'var(--color-border)',
  color: tg?.themeParams?.text_color || 'var(--color-text)',
  backgroundColor: tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
}))
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 200ms; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
