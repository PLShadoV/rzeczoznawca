// Apply the saved appearance before styles paint; all values are allow-listed.
(function () {
  try {
    var saved = JSON.parse(localStorage.getItem("pracownia-v1"));
    var settings = (saved && saved.settings) || {};
    document.documentElement.dataset.theme =
      settings.theme === "dark" ? "dark" : "light";
    document.documentElement.dataset.textSize =
      settings.textSize === "large" ? "large" : "normal";
    document.documentElement.style.colorScheme =
      settings.theme === "dark" ? "dark" : "light";
  } catch (_) {
    /* Storage is optional; the application uses readable defaults. */
  }
})();
