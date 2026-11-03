
const CACHE_NAME = "mindbloom-static-v1";

const STATIC_ASSETS = [
    "/static/css/style.css",
    "/static/images/pwa-192.png",
    "/static/images/pwa-512.png",
    "/static/manifest.json"
];

// Install service worker and cache public static assets
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(STATIC_ASSETS);
        })
    );

    self.skipWaiting();
});

// Activate service worker and remove old caches
self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(name => name.startsWith("mindbloom-static-") && name !== CACHE_NAME)
                    .map(name => caches.delete(name))
            );
        })
    );

    self.clients.claim();
});

// Handle network requests
self.addEventListener("fetch", event => {
    const request = event.request;
    const url = new URL(request.url);

    // Only handle requests from this website
    if (url.origin !== self.location.origin) {
        return;
    }

    // Never cache POST requests or other non-GET requests
    if (request.method !== "GET") {
        return;
    }

    // Cache-first strategy for static resources only
    if (url.pathname.startsWith("/static/")) {
        event.respondWith(
            caches.match(request).then(cachedResponse => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(request).then(response => {
                    if (response.ok) {
                        const responseCopy = response.clone();

                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(request, responseCopy);
                        });
                    }

                    return response;
                });
            })
        );

        return;
    }

    // Network-only for HTML pages and all other requests.
    // Never store private user information.
    if (request.mode === "navigate") {
        event.respondWith(
            fetch(request).catch(() => {
                return caches.match("/offline/");
            })
        );
    }
});
