const CACHE_PREFIX = "vedanta-shell-";
const CACHE = `${CACHE_PREFIX}__BUILD_ID__`;
const SHELL = [
  "/",
  "/index.html",
  "/manifest.webmanifest",
  "/assets/vendor/katex-0.19.1/katex.min.css",
  "/assets/vendor/katex-0.19.1/katex.min.js",
  "/assets/style.css?v=20261028-performance-audio-v1",
  "/assets/gita.css?v=20260827-vsn-borderless-table-v3",
  "/assets/app.js?v=20261028-performance-audio-v1",
  "/assets/pwa.js?v=20261028-pwa-v2",
  "/assets/media-session.js?v=20261028-audio-v1",
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
  // Native media networking understands byte ranges and streaming. A full-body
  // shell-cache response cannot satisfy Safari's range probes correctly, and
  // caching recordings can evict the application shell on smaller devices.
  if (event.request.headers.has("range")
    || event.request.destination === "audio" || event.request.destination === "video"
    || /\.(?:mp3|m4a|mp4|ogg|opus|wav|webm)$/i.test(url.pathname)) return;

  const cacheKey = event.request.mode === "navigate"
    ? new Request(url.origin + url.pathname)
    : event.request;

  const cachedResponse = () => caches.open(CACHE).then(cache => cache.match(cacheKey));
  const remember = response => {
    if (response.status === 200) {
      const copy = response.clone();
      event.waitUntil(caches.open(CACHE).then(cache => cache.put(cacheKey, copy)).catch(() => {}));
    }
    return response;
  };

  // Versioned build assets and data are immutable within one deployment.
  // Serve them from the active build cache on repeat launches instead of
  // re-downloading hundreds of JSON responses every time the PWA opens.
  const buildVersioned = url.searchParams.has("v")
    && (url.pathname.startsWith("/assets/")
      || url.pathname.startsWith("/data/")
      || url.pathname.startsWith("/gita/"));
  if (buildVersioned) {
    event.respondWith(
      cachedResponse().catch(() => undefined).then(cached => cached ||
        fetch(event.request).then(remember)
      )
    );
    return;
  }

  event.respondWith(
    fetch(event.request, { cache: "no-cache" })
      .then(remember)
      .catch(() => cachedResponse())
  );
});
