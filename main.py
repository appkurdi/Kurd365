import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import json

baghdad_tz = timezone(timedelta(hours=3))
today_date = datetime.now(baghdad_tz).strftime('%Y-%m-%d')

comps = "7,11,17,25,572,573,6822"
url = f"https://webws.365scores.com/web/games/current/?appTypeId=5&langId=27&timezoneName=Asia/Baghdad&competitions={comps}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json()
except Exception as e:
    data = {}

def get_smart_stream_link(team_a, team_b):
    sources = [
        "https://syriashdab.com/", "https://score808.live/", "https://yalla-shoot.video/",
        "https://live.kora-star.tv/", "https://www.kooora365.com/", "https://as-goal.com/"
    ]
    ignore_words = ["نادي", "ال", "اف", "سي", "فريق"]
    words_a = [w for w in team_a.split() if len(w) > 2 and w not in ignore_words]
    words_b = [w for w in team_b.split() if len(w) > 2 and w not in ignore_words]
    
    for base_url in sources:
        try:
            req = requests.get(base_url, headers=headers, timeout=8)
            soup = BeautifulSoup(req.text, 'html.parser')
            match_page_url = ""
            for a_tag in soup.find_all('a', href=True):
                text = a_tag.get_text(separator=' ', strip=True)
                href = a_tag['href']
                match_found = any(w in text for w in words_a + words_b)
                if match_found and ("facebook" not in href and "twitter" not in href):
                    match_page_url = href if href.startswith('http') else base_url.rstrip('/') + '/' + href.lstrip('/')
                    break
            
            if match_page_url:
                page_req = requests.get(match_page_url, headers=headers, timeout=8)
                page_soup = BeautifulSoup(page_req.text, 'html.parser')
                for iframe in page_soup.find_all('iframe'):
                    src = iframe.get('src', '')
                    if src and "facebook" not in src and "twitter" not in src and "youtube" not in src:
                        return src
                return match_page_url
        except: continue
    return ""

html_content = """<!DOCTYPE html>
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
    
    <title>Kurd365 - ئەپی وەرزشی</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
        :root { --bg-color: #080808; --card-bg: rgba(26, 26, 28, 0.6); --card-border: rgba(255, 255, 255, 0.06); --text-main: #ffffff; --text-sub: #9ca3af; --accent: #00f2fe; --accent-gradient: linear-gradient(135deg, #4facfe, #00f2fe); --live-btn: linear-gradient(135deg, #ff0844, #ffb199); }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; margin: 0; padding: 0; }
        
        /* لابردنی بۆشایی سەرەوە بۆ ئەوەی ڤیدیۆکە بچێتە سەرەوەی شاشەکە */
        body { font-family: 'Cairo', sans-serif; background-color: var(--bg-color); color: var(--text-main); padding-top: 0; padding-bottom: 85px; min-height: 100vh; }
        
        /* دیزاینی بەشی ڤیدیۆکەی سەرەوە (Hero Section) */
        .hero-section { position: relative; width: 100%; height: 250px; overflow: hidden; display: flex; flex-direction: column; }
        .hero-video { position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translateX(-50%) translateY(-50%); z-index: 1; object-fit: cover; opacity: 0.6; }
        .hero-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(8,8,8,0.3) 0%, rgba(8,8,8,1) 100%); z-index: 2; }
        
        .hero-content { position: relative; z-index: 3; width: 100%; max-width: 500px; margin: 0 auto; padding: 20px 15px; display: flex; justify-content: space-between; align-items: flex-start; margin-top: env(safe-area-inset-top); }
        .logo-wrapper { display: flex; align-items: center; gap: 8px; }
        .header-logo { width: 35px; height: 35px; object-fit: contain; filter: drop-shadow(0 2px 8px rgba(0,242,254,0.4)); }
        .hero-content h1 { font-size: 26px; font-weight: 900; letter-spacing: 0.5px; color: #fff; margin: 0; display: flex; align-items: center; font-family: system-ui, -apple-system, sans-serif; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
        .hero-content h1 .highlight { background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .live-indicator { display: flex; align-items: center; gap: 6px; background: rgba(255, 8, 68, 0.2); border: 1px solid rgba(255, 8, 68, 0.3); padding: 5px 12px; border-radius: 15px; font-size: 11px; font-weight: 800; color: #ff0844; letter-spacing: 1px; backdrop-filter: blur(5px); box-shadow: 0 2px 10px rgba(255, 8, 68, 0.2); }
        .pulse-dot { width: 6px; height: 6px; background-color: #ff0844; border-radius: 50%; animation: pulse-live 1.5s infinite; }
        
        /* هێنانە سەرەوەی یارییەکان بۆ ئەوەی بکەونە سەر سێبەری ڤیدیۆکە */
        .container { max-width: 500px; margin: -50px auto 0; padding: 0 12px; position: relative; z-index: 10; }
        .date-title { font-size: 15px; font-weight: 800; margin-bottom: 15px; color: #fff; display: flex; align-items: center; gap: 8px; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
        .date-title::before { content: ''; display: block; width: 4px; height: 16px; background: var(--accent); border-radius: 4px; box-shadow: 0 0 8px var(--accent); }
        
        .match-card { background: var(--card-bg); border-radius: 14px; margin-bottom: 15px; border: 1px solid var(--card-border); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); overflow: hidden; transition: transform 0.2s ease; }
        .match-card:active { transform: scale(0.98); }
        
        .league-badge { display: flex; align-items: center; justify-content: center; gap: 8px; background: rgba(255,255,255,0.03); padding: 8px; border-bottom: 1px solid var(--card-border); }
        .league-badge img { width: 20px; height: 20px; object-fit: contain; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.3)); }
        .league-badge span { font-size: 12px; font-weight: 800; color: var(--text-sub); font-family: system-ui, sans-serif; letter-spacing: 0.3px; }
        
        .teams-wrapper { display: flex; justify-content: space-between; align-items: center; padding: 15px 10px; }
        .team { display: flex; flex-direction: column; align-items: center; width: 32%; gap: 8px; }
        .team img { width: 45px; height: 45px; object-fit: contain; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); }
        .team span { font-weight: 700; font-size: 11px; text-align: center; line-height: 1.4; }
        
        .match-info { width: 36%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .match-time { font-size: 20px; font-weight: 900; font-family: system-ui, -apple-system, sans-serif; letter-spacing: 0.5px;}
        
        .channel-tag { margin-top: 6px; font-size: 10px; font-weight: 700; background: rgba(0, 242, 254, 0.08); color: var(--accent); padding: 4px 12px; border-radius: 12px; border: 1px solid rgba(0, 242, 254, 0.15); text-align: center; white-space: nowrap; display: flex; align-items: center; justify-content: center; gap: 5px;}
        .channel-tag img { width: 14px; height: 14px; object-fit: contain; }
        
        .action-area { padding: 12px; background: rgba(0,0,0,0.2); border-top: 1px solid var(--card-border); display: flex; justify-content: center; align-items: center; min-height: 52px; }
        .countdown { font-size: 13px; font-weight: 800; color: var(--accent); direction: ltr; display: none; background: rgba(0, 242, 254, 0.05); padding: 6px 14px; border-radius: 15px;}
        .btn-live { display: none; background: var(--live-btn); color: white; padding: 8px 24px; border-radius: 20px; font-size: 13px; font-weight: 800; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(255, 8, 68, 0.3); animation: pulse-live 2s infinite; transition: 0.2s; }
        .btn-live:active { transform: scale(0.95); }
        .btn-disabled { background: #1f2937; color: #6b7280; border: 1px solid #374151; box-shadow: none; animation: none; padding: 8px 24px; border-radius: 20px; font-size: 13px; font-weight: 800; cursor: not-allowed; display: none;}
        .btn-finished { display: none; background: rgba(255, 255, 255, 0.05); color: var(--text-sub); padding: 8px 24px; border-radius: 20px; font-size: 13px; font-weight: 700; border: 1px solid var(--card-border); }
        
        @keyframes pulse-live { 0% { box-shadow: 0 0 0 0 rgba(255, 8, 68, 0.4); } 70% { box-shadow: 0 0 0 8px rgba(255, 8, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 8, 68, 0); } }
        
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 65px; background: rgba(12, 12, 12, 0.9); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-top: 1px solid var(--card-border); display: flex; justify-content: space-around; align-items: center; z-index: 100; padding-bottom: env(safe-area-inset-bottom); }
        .nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--text-sub); text-decoration: none; font-size: 10px; font-weight: 700; transition: 0.3s ease; }
        .nav-item svg { width: 22px; height: 22px; fill: currentColor; }
        .nav-item.active { color: var(--accent); }
        
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; display: none; flex-direction: column; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background: rgba(15,15,15,0.95); border-bottom: 1px solid #222;}
        .modal-title { color: white; font-weight: 700; font-size: 14px; }
        .close-modal { color: white; font-size: 26px; font-weight: 300; cursor: pointer; background: none; border: none; line-height: 1;}
        .modal-body { flex: 1; width: 100%; background: #000; position: relative; }
        .modal-body iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    
    <!-- بەشی ڤیدیۆی سەرەوە -->
    <div class="hero-section">
        <!-- دەتوانیت لینکی ڤیدیۆکە لێرە بگۆڕیت بۆ ڤیدیۆی ڕۆناڵدۆ یان هەر ڤیدیۆیەک -->
        <video class="hero-video" autoplay loop muted playsinline>
            <source src="https://assets.mixkit.co/videos/preview/mixkit-soccer-player-kicking-the-ball-4043-large.mp4" type="video/mp4">
        </video>
        <div class="hero-overlay"></div>
        
        <div class="hero-content">
            <div class="logo-wrapper">
                <img src="https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png" alt="Kurd365 Logo" class="header-logo">
                <h1>Kurd<span class="highlight">365</span></h1>
            </div>
            <div class="live-indicator">
                <span class="pulse-dot"></span> LIVE
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="date-title">یارییەکانی ئەمڕۆ</div>
"""

matches = data.get('games', [])
english_leagues = {
    6822: "Iraq Stars League", 
    572: "UEFA Champions League", 
    7: "Premier League", 
    11: "La Liga", 
    17: "Serie A", 
    25: "Bundesliga"
}
matches_added = 0

for match in matches:
    try:
        match_time = datetime.fromisoformat(match.get('startTime', '').replace('Z', '+00:00'))
        match_baghdad = match_time.astimezone(baghdad_tz)
        if match_baghdad.strftime('%Y-%m-%d') != today_date: continue
        match_timestamp = int(match_time.timestamp() * 1000)
        display_time = match_baghdad.strftime('%H:%M')
    except: continue

    league_id = match.get('competitionId')
    league_name = english_leagues.get(league_id)
    if not league_name: continue
    
    league_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_48,h_48,c_limit,q_auto/v2/Competitions/{league_id}"
    
    home_team = match['homeCompetitor']['name']
    away_team = match['awayCompetitor']['name']
    home_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_96,h_96,c_limit,q_auto/v2/Competitors/{match['homeCompetitor']['id']}"
    away_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_96,h_96,c_limit,q_auto/v2/Competitors/{match['awayCompetitor']['id']}"
    
    stream_link = get_smart_stream_link(home_team, away_team)
    matches_added += 1

    if not stream_link or stream_link == "#":
        btn_html, has_link = f"""<button class="btn-disabled" disabled>لینک ئامادە نییە</button>""", "false"
    else:
        btn_html, has_link = f"""<button class="btn-live" onclick="openPlayer('{stream_link}', '{home_team} - {away_team}')">ڕاستەوخۆ 🔴</button>""", "true"

    html_content += f"""
        <div class="match-card" data-time="{match_timestamp}" data-haslink="{has_link}">
            <div class="league-badge" dir="ltr">
                <img src="{league_logo}" alt="{league_name}">
                <span>{league_name}</span>
            </div>
            <div class="teams-wrapper">
                <div class="team"><img src="{home_logo}"><span>{home_team}</span></div>
                <div class="match-info">
                    <div class="match-time">{display_time}</div>
                    <div class="channel-tag" dir="ltr">
                        <img src="https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png" alt="Icon"> 
                        Kurd365 Live
                    </div>
                </div>
                <div class="team"><img src="{away_logo}"><span>{away_team}</span></div>
            </div>
            <div class="action-area">
                <div class="countdown"></div>
                {btn_html}
                <div class="btn-finished">یاری تەواوبوو</div>
            </div>
        </div>
    """

if matches_added == 0:
    html_content += """<div style="text-align:center; margin-top:40px; color:var(--text-sub); font-size:14px;"><h3>هیچ یارییەکی گرنگ بۆ ئەمڕۆ نییە</h3></div>"""

html_content += """
    </div>
    <div class="bottom-nav">
        <a href="#" class="nav-item active"><svg viewBox="0 0 24 24"><path d="M12 3L4 9v12h5v-7h6v7h5V9z"/></svg><span>یارییەکان</span></a>
        <a href="https://t.me/mtv_ibrahim_app" target="_blank" class="nav-item"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.97 1.25-5.56 3.67-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.06-.49-.83-.27-1.49-.41-1.43-.87.03-.24.36-.48 1-.74 3.92-1.7 6.54-2.83 7.86-3.38 3.74-1.56 4.51-1.83 5.02-1.84.11 0 .36.03.52.16.13.11.17.26.19.37.02.05.02.26.01.4z"/></svg><span>تێلیگرام</span></a>
        <a href="#" class="nav-item" onclick="alert('Kurd365 Live App\\nپەخشی ڕاستەوخۆ')"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg><span>دەربارە</span></a>
    </div>
    <div id="videoModal" class="modal">
        <div class="modal-header"><div class="modal-title" id="modalTitle" dir="ltr">Live Match</div><button class="close-modal" onclick="closePlayer()">&times;</button></div>
        <div class="modal-body"><iframe id="videoIframe" src="" allow="autoplay; encrypted-media; fullscreen" allowfullscreen="true" scrolling="no"></iframe></div>
    </div>
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('sw.js');
        }
        function updateUI() {
            const now = new Date().getTime();
            document.querySelectorAll('.match-card').forEach(card => {
                const diff = parseInt(card.getAttribute('data-time')) - now;
                const hL = card.getAttribute('data-haslink') === 'true';
                const tEl = card.querySelector('.countdown'), lB = card.querySelector('.btn-live'), dB = card.querySelector('.btn-disabled'), fB = card.querySelector('.btn-finished');
                if (diff > 0) {
                    let h = Math.floor(diff / 3600000), m = Math.floor((diff % 3600000) / 60000), s = Math.floor((diff % 60000) / 1000);
                    tEl.innerHTML = `⏳ ${h<10?'0'+h:h}:${m<10?'0'+m:m}:${s<10?'0'+s:s}`;
                    tEl.style.display = 'inline-block'; if(lB) lB.style.display = 'none'; if(dB) dB.style.display = 'none'; fB.style.display = 'none';
                } else if (diff <= 0 && diff > -7200000) { 
                    tEl.style.display = 'none'; fB.style.display = 'none'; 
                    if(hL && lB) { lB.style.display = 'inline-block'; if(dB) dB.style.display = 'none'; }
                    else if(dB) { dB.style.display = 'inline-block'; if(lB) lB.style.display = 'none'; }
                } else {
                    tEl.style.display = 'none'; if(lB) lB.style.display = 'none'; if(dB) dB.style.display = 'none'; fB.style.display = 'inline-block';
                }
            });
        }
        updateUI(); setInterval(updateUI, 1000);
        function openPlayer(link, title) { document.getElementById('modalTitle').innerText = title; document.getElementById('videoIframe').src = link; document.getElementById('videoModal').style.display = 'flex'; document.body.style.overflow = 'hidden'; }
        function closePlayer() { document.getElementById('videoModal').style.display = 'none'; document.getElementById('videoIframe').src = ""; document.body.style.overflow = 'auto'; }
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

manifest_json = f"""{{
  "name": "Kurd365 Live",
  "short_name": "Kurd365",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#080808",
  "theme_color": "#080808",
  "icons": [
    {{
      "src": "https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png",
      "sizes": "192x192",
      "type": "image/png"
    }},
    {{
      "src": "https://i.postimg.cc/YSMK1q9K/1000015352-removebg-preview-(1).png",
      "sizes": "512x512",
      "type": "image/png"
    }}
  ]
}}"""
with open("manifest.json", "w", encoding="utf-8") as file:
    file.write(manifest_json)

sw_js = """
self.addEventListener('install', (e) => { self.skipWaiting(); });
self.addEventListener('fetch', (e) => { });
"""
with open("sw.js", "w", encoding="utf-8") as file:
    file.write(sw_js)
