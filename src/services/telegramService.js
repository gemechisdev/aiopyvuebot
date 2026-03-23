/**
 * telegramService.js
 * Wraps the Telegram WebApp JavaScript SDK.
 * Works gracefully in a regular browser (dev mode) with mock data.
 */

const tg = window.Telegram?.WebApp;

/**
 * Apply Telegram theme colours to the document CSS variables.
 * The CSS already uses --tg-theme-* variables as fallbacks in style.css.
 */
function applyTheme() {
  if (!tg) return;
  const p = tg.themeParams ?? {};
  const root = document.documentElement;
  const map = {
    "--tg-theme-bg-color": p.bg_color,
    "--tg-theme-secondary-bg-color": p.secondary_bg_color,
    "--tg-theme-text-color": p.text_color,
    "--tg-theme-hint-color": p.hint_color,
    "--tg-theme-link-color": p.link_color,
    "--tg-theme-button-color": p.button_color,
    "--tg-theme-button-text-color": p.button_text_color,
    "--tg-theme-header-bg-color": p.header_bg_color,
    "--tg-theme-accent-text-color": p.accent_text_color,
    "--tg-theme-section-bg-color": p.section_bg_color,
    "--tg-theme-section-header-text-color": p.section_header_text_color,
    "--tg-theme-subtitle-text-color": p.subtitle_text_color,
    "--tg-theme-destructive-text-color": p.destructive_text_color,
  };
  for (const [cssVar, value] of Object.entries(map)) {
    if (value) root.style.setProperty(cssVar, value);
  }
  // Keep the document body in sync with the Telegram background colour
  if (p.bg_color) document.body.style.backgroundColor = p.bg_color;
}

export default {
  /** Call this once on app mount to signal readiness to Telegram. */
  init() {
    if (tg) {
      tg.ready();
      tg.expand();
      applyTheme();
      // Re-apply theme whenever Telegram changes it (e.g. user switches mode)
      tg.onEvent("themeChanged", applyTheme);
    }
  },

  /** Returns the Telegram WebApp instance (may be undefined outside Telegram). */
  get instance() {
    return tg;
  },

  /** Returns the raw initData string for authenticating API requests. */
  get initData() {
    return tg?.initData ?? "";
  },

  /**
   * Returns the current user's profile.
   * Falls back to a guest object when running outside Telegram.
   */
  getUserData() {
    const user = tg?.initDataUnsafe?.user;
    if (user) {
      return {
        id: user.id,
        first_name: user.first_name,
        last_name: user.last_name ?? null,
        username: user.username ?? null,
        language_code: user.language_code ?? "en",
        isGuest: false,
      };
    }
    // Dev / browser fallback
    const devId =
      localStorage.getItem("tg-dev-user-id") ??
      String(Math.floor(Math.random() * 90_000) + 10_000);
    localStorage.setItem("tg-dev-user-id", devId);
    return {
      id: parseInt(devId),
      first_name: "Dev",
      last_name: "User",
      username: `dev_${devId}`,
      language_code: "en",
      isGuest: true,
    };
  },

  /** Current Telegram theme params. */
  get themeParams() {
    return tg?.themeParams ?? {};
  },

  /**
   * "light" | "dark" — matches Telegram's current colour scheme.
   * Falls back to "light" when outside Telegram.
   */
  get colorScheme() {
    return tg?.colorScheme ?? "light";
  },

  /** True when running inside Telegram. */
  get isInTelegram() {
    return Boolean(tg?.initData);
  },

  // ── Main Button ─────────────────────────────────────────────────────────────

  showMainButton(text, callback) {
    if (!tg) return;
    tg.MainButton.setText(text);
    tg.MainButton.show();
    tg.MainButton.onClick(callback);
  },

  hideMainButton() {
    tg?.MainButton?.hide();
  },

  // ── Back Button ─────────────────────────────────────────────────────────────

  showBackButton(callback) {
    if (!tg) return;
    tg.BackButton.show();
    tg.BackButton.onClick(callback);
  },

  hideBackButton() {
    tg?.BackButton?.hide();
  },

  // ── Haptic feedback ─────────────────────────────────────────────────────────

  haptic(type = "light") {
    tg?.HapticFeedback?.impactOccurred(type);
  },

  // ── Misc ────────────────────────────────────────────────────────────────────

  close() {
    tg ? tg.close() : window.close();
  },

  openLink(url) {
    if (!tg) {
      window.open(url, "_blank");
      return;
    }
    // t.me links must use openTelegramLink; all other URLs use openLink
    if (url.startsWith("https://t.me/") || url.startsWith("tg://")) {
      tg.openTelegramLink(url);
    } else {
      tg.openLink(url);
    }
  },
};
