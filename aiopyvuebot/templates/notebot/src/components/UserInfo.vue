<template>
  <div
    class="flex items-center gap-3 p-4 rounded-2xl mb-4"
    :style="{
      backgroundColor: tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
    }"
  >
    <!-- Avatar -->
    <div
      class="w-11 h-11 rounded-full flex items-center justify-center text-white font-bold text-lg flex-shrink-0"
      style="background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);"
    >
      {{ initials }}
    </div>

    <!-- Info -->
    <div class="flex-1 min-w-0">
      <p
        class="font-semibold leading-tight truncate"
        :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
      >
        {{ fullName }}
        <span v-if="user.isGuest" class="text-xs font-normal opacity-60"> (guest)</span>
      </p>
      <p
        class="text-xs truncate"
        :style="{ color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)' }"
      >
        {{ user.username ? '@' + user.username : 'ID: ' + user.id }}
      </p>
    </div>

    <!-- Note count badge -->
    <div
      class="flex-shrink-0 text-right"
    >
      <p
        class="text-xl font-bold leading-none"
        style="color: #8b5cf6;"
      >
        {{ noteCount }}
      </p>
      <p
        class="text-xs"
        :style="{ color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)' }"
      >
        {{ noteCount === 1 ? 'note' : 'notes' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const tg = window.Telegram?.WebApp

const props = defineProps({
  user: { type: Object, required: true },
  noteCount: { type: Number, default: 0 },
})

const fullName = computed(() =>
  [props.user.first_name, props.user.last_name].filter(Boolean).join(' ')
)

const initials = computed(() =>
  (props.user.first_name?.[0] ?? '') + (props.user.last_name?.[0] ?? '')
)
</script>
