"use strict";
// Increment this version whenever a release changes the offline asset set.
const VERSION = "1.1.1";
const PREFIX = "pracownia:" + new URL(self.registration.scope).pathname + ":";
const CACHE = PREFIX + VERSION;
const CORE = [
  "./",
  "./index.html",
  "./bootstrap.js",
  "./enhancements.js",
  "./app.js",
  "./offline.js",
  "./style.css",
  "./release.css",
  "./questions.json",
  "./legal-bases.json",
  "./explanations.json",
  "./manifest.webmanifest",
  "./assets/favicon.svg",
  "./assets/blueprint.svg",
  "./assets/icon-192.png",
  "./assets/icon-512.png",
  "./assets/icon-180.png",
  "./assets/fonts/fonts.css",
  "./assets/fonts/dm-sans-latin-variable.woff2",
  "./assets/fonts/dm-sans-latin-ext-variable.woff2",
  "./assets/fonts/manrope-latin-variable.woff2",
  "./assets/fonts/manrope-latin-ext-variable.woff2",
];
const PATHS = new Set(
  CORE.map((path) => new URL(path, self.registration.scope).pathname),
);
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((cache) =>
        cache.addAll(
          CORE.map(
            (path) =>
              new Request(new URL(path, self.registration.scope), {
                cache: "reload",
              }),
          ),
        ),
      ),
  );
});
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k.startsWith(PREFIX) && k !== CACHE)
            .map((k) => caches.delete(k)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});
self.addEventListener("message", (event) => {
  if (event.data?.type === "SKIP_WAITING") self.skipWaiting();
});
self.addEventListener("fetch", (event) => {
  const request = event.request,
    url = new URL(request.url);
  if (
    request.method !== "GET" ||
    url.origin !== self.location.origin ||
    !url.href.startsWith(self.registration.scope)
  )
    return;
  if (request.mode !== "navigate" && !PATHS.has(url.pathname)) return;
  event.respondWith(
    (async () => {
      let cache = null;
      try {
        cache = await caches.open(CACHE);
      } catch (_) {
        /* A cache failure must not block online access. */
      }
      // Serve this complete release snapshot until the user accepts an installed update.
      // This keeps app/enhancements/data versions together across reloads.
      if (cache && PATHS.has(url.pathname)) {
        try {
          const stored = await cache.match(request, { ignoreSearch: true });
          if (stored) return stored;
        } catch (_) {}
      }
      try {
        const response = await fetch(request);
        if (!response.ok) throw Error("network response " + response.status);
        // Cache only the public application assets, never arbitrary same-origin URLs.
        if (cache && PATHS.has(url.pathname)) {
          try {
            await cache.put(request, response.clone());
          } catch (_) {
            /* Return the fresh response even if storage is full. */
          }
        }
        return response;
      } catch (error) {
        let cached;
        try {
          cached = cache
            ? await cache.match(request, { ignoreSearch: true })
            : null;
        } catch (_) {}
        if (cached) return cached;
        if (request.mode === "navigate") {
          let index;
          try {
            index = cache
              ? await cache.match(
                  new URL("./index.html", self.registration.scope).href,
                )
              : null;
          } catch (_) {}
          if (index) return index;
        }
        return new Response(
          "Brak połączenia. Otwórz stronę online, aby zapisać ją do nauki offline.",
          {
            status: 503,
            headers: { "Content-Type": "text/plain; charset=utf-8" },
          },
        );
      }
    })(),
  );
});
