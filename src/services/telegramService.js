/**
 * telegramService.js
 * Wraps the Telegram WebApp JavaScript SDK.
 * Works gracefully in a regular browser (dev mode) with mock data.
 */

const tg = window.Telegram?.WebApp;

export default {
  /** Call this once on app mount to signal readiness to Telegram. */
  init() {
    if (tg) {
      tg.ready();
      tg.expand();
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
    tg ? tg.openTelegramLink(url) : window.open(url, "_blank");
  },
};
