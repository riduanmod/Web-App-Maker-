const CACHE_NAME = 'pwa-generator-cache-v1';

const INITIAL_CACHED_RESOURCES = [
  '/',
  '/style.css',
  '/script.js',
  // Note: We don't statically cache /app because its query params change dynamically
];

// Install Event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(INITIAL_CACHED_RESOURCES);
            })
    );
    self.skipWaiting();
});

// Activate Event
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(name => name !== CACHE_NAME)
                          .map(name => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

// Fetch Event (Stale-while-revalidate for dynamic routes)
self.addEventListener('fetch', event => {
    // Exclude API calls or external domains from SW cache if necessary
    if (!event.request.url.startsWith(self.location.origin)) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            if (cachedResponse) {
                // Return cached version but fetch network in background (Stale-While-Revalidate)
                fetch(event.request).then(networkResponse => {
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, networkResponse.clone());
                    });
                }).catch(() => { /* Network failed, silent catch */ });
                return cachedResponse;
            }

            // If not in cache, go to network
            return fetch(event.request).then(networkResponse => {
                return caches.open(CACHE_NAME).then(cache => {
                    cache.put(event.request, networkResponse.clone());
                    return networkResponse;
                });
            }).catch(() => {
                // Basic Offline Fallback HTML
                return new Response(
                    `<html><body style="font-family:sans-serif; text-align:center; padding-top:50px;">
                        <h2>You are offline</h2>
                        <p>Please check your internet connection to access this app.</p>
                     </body></html>`,
                    { headers: { 'Content-Type': 'text/html' } }
                );
            });
        })
    );
});
