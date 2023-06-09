"use strict";
// Cache Name
const CACHE_NAME = "static-cache-v2";
// Cache Files
const FILES_TO_CACHE = [
  "/build/bundle.css",
  "/build/bundle.js",
  "/build/bundle.js.map",
  "/background.avif",
  "/favicon.png",
  "/index.html",
  "/manifest.json",
  "/offline.html",
  "/service-worker.js",
  "/",
];

// install
self.addEventListener("install", (evt) => {
  // console.log("[ServiceWorker] Install");
  evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // console.log("[ServiceWorker] Pre-caching offline page");
      return cache.addAll(FILES_TO_CACHE);
    })
  );
  self.skipWaiting();
});
// Active PWA Cache and clear out anything older
self.addEventListener("activate", (evt) => {
  // console.log("[Service Worker] Activate");
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            // console.log("[Service Worker] Removing old cache", key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});
self.addEventListener("fetch", (e) => {
  if (e.request.method === "GET") {
    e.respondWith(
      (async () => {
        const r = await caches.match(e.request);
        // console.log(`[Service Worker] Fetching resource: ${e.request.url}`);
        if (r && !e.request.url.endsWith("/api")) {
          return r;
        }
        const response = await fetch(e.request);
        const cache = await caches.open(CACHE_NAME);
        // console.log(`[Service Worker] Caching new resource: ${e.request.url}`);

        // check if request is made by chrome extensions or web page
        // if request is made for web page url must contains http.
        // if (!(e.request.url.indexOf('http') === 0)) return; // skip the request. if request is not made with http protocol


        cache.put(e.request, response.clone());
        return response;
      })()
    );
  }
});
