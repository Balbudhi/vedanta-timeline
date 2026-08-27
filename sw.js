const CACHE_PREFIX = "vedanta-shell-";
const CACHE = `${CACHE_PREFIX}__BUILD_ID__`;
const SHELL = [
  "/",
  "/index.html",
  "/manifest.webmanifest",
  "/assets/style.css?v=20260827-mobile-v1",
  "/assets/gita.css",
  "/assets/app.js?v=20260819-encyclopedia-prose-v6",
  "/assets/pwa.js?v=20260827-pwa-v1",
  "/assets/favicon.svg",
  "/assets/favicon.png",
  "/assets/icon-192.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((key) => key.startsWith(CACHE_PREFIX) && key !== CACHE)
          .map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  const cacheKey = event.request.mode === "navigate"
    ? new Request(url.origin + url.pathname)
    : event.request;

  event.respondWith(
    fetch(event.request, { cache: "no-store" })
      .then((response) => {
        if (response.ok) {
          const copy = response.clone();
          event.waitUntil(caches.open(CACHE).then((cache) => cache.put(cacheKey, copy)));
        }
        return response;
      })
      .catch(() => caches.match(cacheKey))
  );
});
