
const CACHE_NAME = 'kurd365-cache-channels-v3';
const urlsToCache = [ './', './index.html', './manifest.json', './video.mp4', 'https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png' ];
self.addEventListener('install', event => { self.skipWaiting(); event.waitUntil( caches.open(CACHE_NAME).then(cache => { return cache.addAll(urlsToCache); }) ); });
self.addEventListener('fetch', event => { event.respondWith( caches.match(event.request).then(response => { if (response) { return response; } return fetch(event.request); }) ); });
