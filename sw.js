const C="shlav-mcq-v36";
const PRE=["./","index.html","questions.json","manifest.webmanifest","icon-192.png","icon-512.png","images/N-I-8-13.jpg","images/N-I-8-30.jpg","images/N-I-8-7.jpg","images/B108-61.jpg","images/B108-62.jpg","images/B108-63.jpg","images/B108-64.jpg","images/B108-65.jpg","images/B108-66.jpg","images/B108-67.jpg","images/B108-68.jpg"];
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>Promise.all(PRE.map(u=>c.add(u).catch(()=>{})))));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r;}).catch(()=>caches.match(e.request).then(m=>m||caches.match("index.html"))));});
