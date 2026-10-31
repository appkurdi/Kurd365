import requests
from bs4 import BeautifulSoup
import re

html_top = """<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#080808">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="Kurd365">
    
    <link rel="apple-touch-icon" href="https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png">
    <link rel="icon" type="image/png" href="https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png">
    
    <title>Kurd365 - کەناڵەکان</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
        :root { --bg-color: #080808; --card-bg: rgba(26, 26, 28, 0.6); --card-border: rgba(255, 255, 255, 0.06); --text-main: #ffffff; --text-sub: #9ca3af; --accent: #00f2fe; --accent-gradient: linear-gradient(135deg, #4facfe, #00f2fe); --live-btn: linear-gradient(135deg, #ff0844, #ffb199); }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; margin: 0; padding: 0; }
        
        body { font-family: 'Cairo', sans-serif; background-color: var(--bg-color); color: var(--text-main); padding-top: 0; padding-bottom: 85px; min-height: 100vh; overflow-x: hidden; }
        
        .hero-section { position: relative; width: 100%; height: 260px; overflow: hidden; display: flex; flex-direction: column; background-color: #080808; }
        .hero-video { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; object-position: center; z-index: 1; opacity: 0.75; transition: opacity 1.5s ease; }
        .hero-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(8,8,8,0.2) 0%, rgba(8,8,8,1) 100%); z-index: 2; transition: background 1.5s ease; }
        
        .hero-content { position: relative; z-index: 4; width: 100%; max-width: 500px; margin: 0 auto; padding: 20px 15px; display: flex; justify-content: space-between; align-items: flex-start; margin-top: env(safe-area-inset-top); }
        .logo-wrapper { display: flex; align-items: center; gap: 8px; }
        .header-logo { width: 35px; height: 35px; object-fit: contain; filter: drop-shadow(0 2px 8px rgba(0,242,254,0.4)); }
        .hero-content h1 { font-size: 26px; font-weight: 900; letter-spacing: 0.5px; color: #fff; margin: 0; display: flex; align-items: center; font-family: system-ui, -apple-system, sans-serif; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
        .hero-content h1 .highlight { background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .container { max-width: 500px; margin: -40px auto 0; padding: 0 12px; position: relative; z-index: 10; }
        .date-title { font-size: 16px; font-weight: 800; margin-bottom: 15px; color: #fff; display: flex; align-items: center; gap: 8px; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
        .date-title::before { content: ''; display: block; width: 4px; height: 16px; background: var(--accent); border-radius: 4px; box-shadow: 0 0 8px var(--accent); }
        
        .channel-card { background: var(--card-bg); border-radius: 14px; margin-bottom: 15px; border: 1px solid var(--card-border); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); padding: 15px; display: flex; align-items: center; justify-content: space-between; transition: transform 0.2s ease; }
        .channel-card:active { transform: scale(0.98); }
        
        .channel-info-wrapper { display: flex; align-items: center; gap: 15px; }
        .channel-icon { width: 45px; height: 45px; background: rgba(0, 242, 254, 0.1); border-radius: 50%; display: flex; justify-content: center; align-items: center; border: 1px solid rgba(0, 242, 254, 0.3); flex-shrink: 0; box-shadow: 0 0 10px rgba(0, 242, 254, 0.1); }
        .channel-icon span { font-size: 22px; font-weight: 900; color: var(--accent); font-family: system-ui, sans-serif; }
        
        .channel-details { display: flex; flex-direction: column; gap: 4px; }
        .channel-name { font-size: 16px; font-weight: 800; color: #fff; letter-spacing: 0.5px; }
        .channel-status { font-size: 11px; font-weight: 700; color: #ff0844; display: flex; align-items: center; gap: 5px; }
        
        .pulse-dot-small { width: 6px; height: 6px; background-color: #ff0844; border-radius: 50%; animation: pulse-live 1.5s infinite; }
        @keyframes pulse-live { 0% { box-shadow: 0 0 0 0 rgba(255, 8, 68, 0.4); } 70% { box-shadow: 0 0 0 8px rgba(255, 8, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 8, 68, 0); } }
        
        .btn-live { background: var(--live-btn); color: white; padding: 8px 18px; border-radius: 20px; font-size: 13px; font-weight: 800; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(255, 8, 68, 0.3); transition: 0.2s; white-space: nowrap; }
        
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 65px; background: rgba(12, 12, 12, 0.9); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-top: 1px solid var(--card-border); display: flex; justify-content: space-around; align-items: center; z-index: 100; padding-bottom: env(safe-area-inset-bottom); }
        .nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--text-sub); text-decoration: none; font-size: 10px; font-weight: 700; transition: 0.3s ease; }
        .nav-item svg { width: 22px; height: 22px; fill: currentColor; }
        .nav-item.active { color: var(--accent); }
        
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; display: none; flex-direction: column; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background: rgba(15,15,15,0.95); border-bottom: 1px solid #222;}
        .modal-title { color: white; font-weight: 700; font-size: 14px; }
        .close-modal { color: white; font-size: 26px; font-weight: 300; cursor: pointer; background: none; border: none; line-height: 1;}
        .modal-body { flex: 1; width: 100%; background: #000; position: relative; }
        .modal-body iframe, .modal-body video { width: 100%; height: 100%; border: none; }
    </style>
    <!-- کتێبخانەی HLS بۆ لێدانی ڕاستەوخۆی m3u8 -->
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body>
    
    <div class="hero-section">
        <video id="heroVideo" class="hero-video" autoplay muted playsinline loop>
            <source src="video.mp4" type="video/mp4">
        </video>
        <div class="hero-overlay" id="heroOverlay"></div>
        <div class="hero-content">
            <div class="logo-wrapper">
                <img src="https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png" alt="Kurd365 Logo" class="header-logo">
                <h1>Kurd<span class="highlight">365</span></h1>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="date-title">کەناڵەکانی ئەلوان سپۆرت</div>
"""

cards_html = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://alwanlive.stream/"
}

# گەڕان بەدوای لینکی ڕاستەقینەدا بۆ هەموو کەناڵەکان
for i in range(1, 11):
    channel_title = f"ئەلوان سپۆرت {i}"
    target_url = f"https://alwanlive.stream/?channel={i}&server=1"
    
    # وەکو یەدەگ سەرەتا لینکە گشتییەکە دادەنێین
    stream_link = target_url
    
    try:
        req = requests.get(target_url, headers=headers, timeout=10)
        
        # ١. هەوڵدەدات لینکی m3u8 بدۆزێتەوە
        m3u8_match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', req.text)
        if m3u8_match:
            stream_link = m3u8_match.group(1)
        else:
            # ٢. ئەگەر نەبوو، هەوڵدەدات لینکی iframe پلەیەرەکە بدۆزێتەوە
            soup = BeautifulSoup(req.text, 'html.parser')
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src', '')
                if src and not any(bad in src.lower() for bad in ['ad', 'facebook', 'twitter']):
                    if src.startswith('//'):
                        stream_link = 'https:' + src
                    elif src.startswith('/'):
                        stream_link = 'https://alwanlive.stream' + src
                    else:
                        stream_link = src
                    break
    except Exception as e:
        pass
    
    cards_html += f"""
        <div class="channel-card">
            <div class="channel-info-wrapper">
                <div class="channel-icon">
                    <span>{i}</span>
                </div>
                <div class="channel-details">
                    <div class="channel-name">{channel_title}</div>
                    <div class="channel-status">
                        <span class="pulse-dot-small"></span> پەخشی ڕاستەوخۆ 24/7
                    </div>
                </div>
            </div>
            <button class="btn-live" onclick="openPlayer('{stream_link}', '{channel_title}')">
                سەیرکردن
            </button>
        </div>
    """

html_bottom = """
    </div>
    
    <div class="bottom-nav">
        <a href="#" class="nav-item active"><svg viewBox="0 0 24 24"><path d="M21 3H3c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5c0-1.1-.9-2-2-2zm0 14H3V5h18v12z"/></svg><span>کەناڵەکان</span></a>
        <a href="https://t.me/mtv_ibrahim_app" target="_blank" class="nav-item"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.97 1.25-5.56 3.67-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.06-.49-.83-.27-1.49-.41-1.43-.87.03-.24.36-.48 1-.74 3.92-1.7 6.54-2.83 7.86-3.38 3.74-1.56 4.51-1.83 5.02-1.84.11 0 .36.03.52.16.13.11.17.26.19.37.02.05.02.26.01.4z"/></svg><span>تێلیگرام</span></a>
        <a href="#" class="nav-item" onclick="alert('Kurd365 Live Channels\\nئەپی پەخشی ڕاستەوخۆ')"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg><span>دەربارە</span></a>
    </div>
    
    <div id="videoModal" class="modal">
        <div class="modal-header">
            <div class="modal-title" id="modalTitle" dir="rtl">پەخشی ڕاستەوخۆ</div>
            <button class="close-modal" onclick="closePlayer()">&times;</button>
        </div>
        <div class="modal-body">
            <!-- ئەگەر لینکەکە iframe بوو ئەمە کار دەکات -->
            <iframe id="videoIframe" src="" allow="autoplay; encrypted-media; fullscreen" allowfullscreen="true" scrolling="no" style="display: none;"></iframe>
            <!-- ئەگەر لینکەکە m3u8 بوو ئەمە کار دەکات -->
            <video id="videoPlayer" controls autoplay style="display: none;"></video>
        </div>
    </div>
    
    <script>
        if ('serviceWorker' in navigator) { navigator.serviceWorker.register('sw.js'); }
        
        function openPlayer(link, title) { 
            document.getElementById('modalTitle').innerText = title; 
            document.getElementById('videoModal').style.display = 'flex'; 
            document.body.style.overflow = 'hidden'; 
            
            const iframe = document.getElementById('videoIframe');
            const video = document.getElementById('videoPlayer');
            
            // زیرەکی جاڤاسکڕیپت: زانینی جۆری لینکەکە
            if (link.includes('.m3u8')) {
                iframe.style.display = 'none';
                video.style.display = 'block';
                
                if (Hls.isSupported()) {
                    var hls = new Hls();
                    hls.loadSource(link);
                    hls.attachMedia(video);
                    hls.on(Hls.Events.MANIFEST_PARSED, function() {
                        video.play();
                    });
                } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                    video.src = link;
                    video.addEventListener('loadedmetadata', function() {
                        video.play();
                    });
                }
            } else {
                video.style.display = 'none';
                iframe.style.display = 'block';
                iframe.src = link;
            }
        }
        
        function closePlayer() { 
            document.getElementById('videoModal').style.display = 'none'; 
            document.getElementById('videoIframe').src = ""; 
            
            const video = document.getElementById('videoPlayer');
            video.pause();
            video.removeAttribute('src');
            
            document.body.style.overflow = 'auto'; 
        }
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_top + cards_html + html_bottom)

sw_js = """
const CACHE_NAME = 'kurd365-cache-channels-v3';
const urlsToCache = [ './', './index.html', './manifest.json', './video.mp4', 'https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png' ];
self.addEventListener('install', event => { self.skipWaiting(); event.waitUntil( caches.open(CACHE_NAME).then(cache => { return cache.addAll(urlsToCache); }) ); });
self.addEventListener('fetch', event => { event.respondWith( caches.match(event.request).then(response => { if (response) { return response; } return fetch(event.request); }) ); });
"""

with open("sw.js", "w", encoding="utf-8") as file:
    file.write(sw_js)
