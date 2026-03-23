<template>
  <div class="min-h-screen p-4 relative">
    <!-- Background patterns -->
    <div class="fixed inset-0 pattern-dots opacity-5 pointer-events-none"></div>

    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <header class="text-center mb-8">
        <div class="relative inline-block mb-4">
          <div
            class="w-24 h-24 rounded-full flex items-center justify-center text-4xl shadow-lg mx-auto"
            :style="{
              background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
            }"
          >
            🔒
          </div>
          <div
            class="absolute -top-2 -right-2 w-8 h-8 rounded-full flex items-center justify-center text-sm shadow-md"
            style="background: linear-gradient(135deg, #10b981 0%, #34d399 100%); color: white;"
          >
            ✓
          </div>
        </div>
        
        <h1
          class="text-3xl font-bold mb-2"
          :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
        >
          🔒 WhispierBot
        </h1>
        <p
          class="text-lg"
          :style="{
            color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
          }"
        >
          Send secret messages that only specific people can read
        </p>
      </header>

      <!-- Main Content -->
      <div class="space-y-6">
        <!-- Welcome Message -->
        <div
          class="card p-6 rounded-2xl relative overflow-hidden"
          :style="{
            backgroundColor: tg?.themeParams?.bg_color || 'var(--color-bg)',
            boxShadow: 'var(--shadow-lg)',
          }"
        >
          <div
            class="pattern-dots absolute inset-0 opacity-5 pointer-events-none"
          ></div>
          <div class="relative z-10">
            <h2
              class="text-xl font-bold mb-4 flex items-center gap-2"
              :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
            >
              <span class="text-2xl">👋</span>
              Welcome to WhispierBot!
            </h2>
            <p
              class="leading-relaxed mb-4"
              :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
            >
              I help you send secret messages (whispers) that only specific people can read, 
              even in public groups and chats! Your messages are secure and private.
            </p>
            <div
              class="p-4 rounded-lg"
              :style="{
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                border: '1px solid rgba(139, 92, 246, 0.2)',
              }"
            >
              <p class="text-sm font-medium" style="color: #8b5cf6;">
                💡 Perfect for sending private messages in group chats without anyone else seeing them!
              </p>
            </div>
          </div>
        </div>

        <!-- How to Use -->
        <div
          class="card p-6 rounded-2xl relative overflow-hidden"
          :style="{
            backgroundColor:
              tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
            boxShadow: 'var(--shadow-md)',
          }"
        >
          <h3
            class="text-lg font-bold mb-4 flex items-center gap-2"
            :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
          >
            <span class="text-xl">📖</span>
            How to Use
          </h3>
          <div class="space-y-3">
            <div
              v-for="(step, index) in steps"
              :key="index"
              class="flex items-start gap-3"
            >
              <div
                class="w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold text-white flex-shrink-0 mt-1"
                :style="{ background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)' }"
              >
                {{ index + 1 }}
              </div>
              <p
                class="text-sm leading-relaxed"
                :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
              >
                {{ step }}
              </p>
            </div>
          </div>
        </div>

        <!-- Example -->
        <div
          class="card p-6 rounded-2xl relative overflow-hidden"
          :style="{
            backgroundColor: tg?.themeParams?.bg_color || 'var(--color-bg)',
            boxShadow: 'var(--shadow-md)',
          }"
        >
          <h3
            class="text-lg font-bold mb-4 flex items-center gap-2"
            :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
          >
            <span class="text-xl">💬</span>
            Example
          </h3>
          <div
            class="p-4 rounded-lg font-mono text-sm"
            :style="{
              backgroundColor: 'rgba(0, 0, 0, 0.05)',
              border: '1px dashed rgba(139, 92, 246, 0.3)',
            }"
          >
            <span style="color: #8b5cf6;">@whispierbot</span>
            <span :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }">
              This is a secret message 
            </span>
            <span style="color: #ec4899;">@username</span>
          </div>
          <p
            class="text-xs mt-2"
            :style="{
              color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
            }"
          >
            Only @username will be able to open and read this message!
          </p>
        </div>

        <!-- Features -->
        <div
          class="card p-6 rounded-2xl relative overflow-hidden"
          :style="{
            backgroundColor:
              tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
            boxShadow: 'var(--shadow-md)',
          }"
        >
          <h3
            class="text-lg font-bold mb-4 flex items-center gap-2"
            :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
          >
            <span class="text-xl">✨</span>
            Features
          </h3>
          <div class="grid grid-cols-2 gap-3">
            <div
              v-for="feature in features"
              :key="feature.text"
              class="flex items-center gap-2"
            >
              <span class="text-lg">{{ feature.icon }}</span>
              <span
                class="text-sm"
                :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
              >
                {{ feature.text }}
              </span>
            </div>
          </div>
        </div>

        <!-- Try It Button -->
        <div class="text-center">
          <button
            @click="openBot"
            class="inline-flex items-center gap-2 px-8 py-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 font-medium"
            :style="{
              background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
              color: '#ffffff',
            }"
          >
            <span class="text-xl">🔒</span>
            Try WhispierBot Now
          </button>
        </div>

        <!-- Footer -->
        <div class="text-center py-6">
          <p
            class="text-sm"
            :style="{
              color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
            }"
          >
            Built with ❤️ using PyVueBot by 
            <a
              href="https://t.me/venopyx"
              class="font-medium"
              style="color: #8b5cf6;"
            >
              @venopyx
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const tg = window.Telegram?.WebApp;

const steps = [
  "Type @whispierbot in any chat or group",
  "Write your secret message",
  "Add the recipient's @username or ID at the end", 
  "Send it - only they can open the whisper!"
];

const features = [
  { icon: "✅", text: "Works anywhere" },
  { icon: "🔐", text: "Secure & private" },
  { icon: "👥", text: "Group compatible" },
  { icon: "⏰", text: "Auto-expires" },
  { icon: "🚀", text: "Fast & reliable" },
  { icon: "🆓", text: "Completely free" }
];

const openBot = () => {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.openTelegramLink("https://t.me/whispierbot");
  } else {
    window.open("https://t.me/whispierbot", "_blank");
  }
};
</script>

<style scoped>
.pattern-dots {
  background-image: radial-gradient(
    rgba(139, 92, 246, 0.1) 1px,
    transparent 1px
  );
  background-size: 20px 20px;
  background-position: 0 0;
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
}
</style>