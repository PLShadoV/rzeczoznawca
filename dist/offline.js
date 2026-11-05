"use strict";
// Progressive enhancement: regular learning does not depend on service-worker support.
if (
  "serviceWorker" in navigator &&
  (location.protocol === "https:" ||
    ["localhost", "127.0.0.1", "[::1]"].includes(location.hostname))
) {
  window.addEventListener("load", () => {
    let updateRequested = false;
    navigator.serviceWorker
      .register("./sw.js")
      .then((registration) => {
        const offerUpdate = () => {
          if (!registration.waiting) return;
          const banner = document.getElementById("update-banner"),
            button = document.getElementById("update-app");
          if (!banner || !button) return;
          banner.hidden = false;
          button.onclick = () => {
            // Saving through the app preserves the current selections before a user-requested reload.
            if (typeof save === "function" && save() === false) {
              if (typeof toast === "function")
                toast(
                  "Przed odświeżeniem pobierz kopię w Statystykach — trwały zapis jest niedostępny.",
                );
              return;
            }
            updateRequested = true;
            button.disabled = true;
            registration.waiting.postMessage({ type: "SKIP_WAITING" });
          };
        };
        offerUpdate();
        registration.addEventListener("updatefound", () => {
          const worker = registration.installing;
          worker?.addEventListener("statechange", () => {
            if (
              worker.state === "installed" &&
              navigator.serviceWorker.controller
            )
              offerUpdate();
          });
        });
      })
      .catch(() => {
        /* Offline support is optional; the online application continues normally. */
      });
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (updateRequested) location.reload();
    });
  });
}
window.addEventListener("offline", () => {
  if (typeof toast === "function")
    toast(
      "Brak połączenia. Zapisany postęp nadal działa; zewnętrzne źródła wymagają internetu.",
    );
});
window.addEventListener("online", () => {
  if (typeof toast === "function") toast("Połączenie przywrócone.");
});
