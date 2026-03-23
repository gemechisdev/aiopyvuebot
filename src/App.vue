<template>
  <BotInfo />
</template>

<script setup>
import BotInfo from "./components/BotInfo.vue";

// Initialize Telegram Mini App if available
if (window.Telegram?.WebApp) {
  window.Telegram.WebApp.ready();
  window.Telegram.WebApp.expand();
}
</script>