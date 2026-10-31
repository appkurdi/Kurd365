import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# کاتی بەغدا
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
    print("Error fetching data:", e)
    data = {}

def get_smart_stream_link(team_a, team_b):
    sources = [
        "https://syriashdab.com/",
        "https://score808.live/",
        "https://yalla-shoot.video/",
        "https://live.kora-star.tv/",
        "https://www.kooora365.com/",
        "https://as-goal.com/"
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
                match_found = False
                for w in words_a + words_b:
                    if w in text:
                        match_found = True
                        break
                if match_found and ("facebook" not in href and "twitter" not in href):
                    match_page_url = href if href.startswith('http') else base_url.rstrip('/') + '/' + href.lstrip('/')
                    break
            
            if match_page_url:
                page_req = requests.get(match_page_url, headers=headers, timeout=8)
                page_soup = BeautifulSoup(page_req.text, 'html.parser')
                iframes = page_soup.find_all('iframe')
                for iframe in iframes:
                    src = iframe.get('src', '')
                    if src and "facebook" not in src and "twitter" not in src and "youtube" not in src:
                        return src
                return match_page_url
        except:
            continue
    return ""

html_content = """
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    
    <!-- PWA & Web App Meta Tags -->
    <meta name="theme-color" content="#0d0d0d">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="Kurd365">
    
    <title>Kurd365 - ئەپی وەرزشی</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
        
        :root {
            --bg-color: #080808;
            --card-bg: rgba(26, 26, 28, 0.7);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-main: #ffffff;
            --text-sub: #9ca3af;
            --accent: #00f2fe;
            --accent-gradient: linear-gradient(135deg, #4facfe, #00f2fe);
            --live-btn: linear-gradient(135deg, #ff0844, #ffb199);
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Cairo', sans-serif; 
            background-color: var(--bg-color); 
            color: var(--text-main); 
            padding-top: 80px; 
            padding-bottom: 90px; 
            min-height: 100vh;
        }
        
        /* هێدەری سەرەوە - دیزاینی شووشەیی (Glassmorphism) */
        .header { 
            position: fixed; top: 0; left: 0; width: 100%; height: 65px; z-index: 100; 
            background: rgba(8, 8, 8, 0.75); 
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            display: flex; align-items: center; justify-content: center; 
            border-bottom: 1px solid var(--card-border); 
        }
        .header h1 { 
            font-size: 26px; font-weight: 900; letter-spacing: 1px;
            background: var(--accent-gradient); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        }
        
        .container { max-width: 600px; margin: 0 auto; padding: 0 15px; }
        .date-title { font-size: 16px; font-weight: 800; margin-bottom: 20px; color: var(--text-sub); display: flex; align-items: center; gap: 8px;}
        .date-title::before { content: ''; display: block; width: 4px; height: 16px; background: var(--accent); border-radius: 4px; }

        /* کارتی یارییەکان - ڕێسپۆنسڤ و مۆدێرن */
        .match-card { 
            background: var(--card-bg); 
            border-radius: 20px; 
            margin-bottom: 20px; 
            border: 1px solid var(--card-border); 
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            overflow: hidden; 
            transition: transform 0.2s ease;
        }
        .match-card:active { transform: scale(0.98); }
        
        .league-badge { 
            background: rgba(255,255,255,0.03); 
            padding: 10px; font-size: 12px; font-weight: 800; 
            color: var(--text-sub); text-align: center; 
            border-bottom: 1px solid var(--card-border); 
        }
        
        .teams-wrapper { display: flex; justify-content: space-between; align-items: center; padding: 20px 15px; }
        .team { display: flex; flex-direction: column; align-items: center; width: 33%; gap: 10px; }
        .team img { width: 55px; height: 55px; object-fit: contain; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); }
        .team span { font-weight: 800; font-size: 13px; text-align: center; line-height: 1.4; }
        
        .match-info { width: 34%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .match-time { font-size: 24px; font-weight: 900; font-family: system-ui, -apple-system, sans-serif; letter-spacing: 0.5px;}
        .channel-tag { 
            margin-top: 8px; font-size: 10px; font-weight: 700;
            background: rgba(0, 242, 254, 0.1); color: var(--accent); 
            padding: 4px 10px; border-radius: 12px; 
            border: 1px solid rgba(0, 242, 254, 0.2); 
            text-align: center; white-space: nowrap;
        }

        .action-area { 
            padding: 15px; background: rgba(0,0,0,0.2); 
            border-top: 1px solid var(--card-border); 
            display: flex; justify-content: center; align-items: center; min-height: 65px;
        }
        
        .countdown { font-size: 14px; font-weight: 800; color: var(--accent); direction: ltr; display: none; background: rgba(0, 242, 254, 0.05); padding: 8px 16px; border-radius: 20px;}
        
        .btn-live { 
            display: none; background: var(--live-btn); color: white; 
            padding: 10px 28px; border-radius: 30px; font-size: 14px; font-weight: 800; 
            border: none; cursor: pointer; 
            box-shadow: 0 4px 15px rgba(255, 8, 68, 0.4);
            animation: pulse-live 2s infinite; 
            transition: 0.2s;
        }
        .btn-live:active { transform: scale(0.95); }
        
        .btn-disabled { background: #1f2937; color: #6b7280; border: 1px solid #374151; box-shadow: none; animation: none; padding: 10px 28px; border-radius: 30px; font-size: 14px; font-weight: 800; cursor: not-allowed; display: none;}
        .btn-finished { display: none; background: rgba(255, 255, 255, 0.05); color: var(--text-sub); padding: 10px 28px; border-radius: 30px; font-size: 14px; font-weight: 700; border: 1px solid var(--card-border); }

        @keyframes pulse-live { 0% { box-shadow: 0 0 0 0 rgba(255, 8, 68, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(255, 8, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 8, 68, 0); } }

        /* شریتی خوارەوە (Bottom Navigation) تایبەت بە ئەپ */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
            background: rgba(15, 15, 15, 0.85); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border-top: 1px solid var(--card-border);
            display: flex; justify-content: space-around; align-items: center;
            z-index: 100; padding-bottom: env(safe-area-inset-bottom);
        }
        .nav-item {
            display: flex; flex-direction: column; align-items: center; gap: 4px;
            color: var(--text-sub); text-decoration: none; font-size: 11px; font-weight: 700;
            transition: 0.3s ease;
        }
        .nav-item svg { width: 24px; height: 24px; fill: currentColor; }
        .nav-item.active { color: var(--accent); }

        /* پلەیەری ڤیدیۆ مۆدێرن */
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; display: none; flex-direction: column; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: rgba(20,20,20,0.9); border-bottom: 1px solid #333;}
        .modal-title { color: white; font-weight: 800; font-size: 15px; }
        .close-modal { color: white; font-size: 30px; font-weight: 300; cursor: pointer; background: none; border: none; line-height: 1;}
        .modal-body { flex: 1; width: 100%; background: #000; position: relative; }
        .modal-body iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>

    <div class="header"><h1>Kurd365</h1></div>
    
    <div class="container">
        <div class="date-title">یارییەکانی ئەمڕۆ</div>
"""

matches = data.get('games', [])
kurdish_leagues = {
    6822: "خولی ئەستێرەکانی عێراق", 572: "چامپیۆنزلیگ", 7: "پریمەرلیگ", 
    11: "لالیگا", 17: "خولی ئیتاڵی", 25: "خولی ئەڵمانی"
}

matches_added = 0

for match in matches:
    try:
        start_time_str = match.get('startTime', '')
        match_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        match_baghdad = match_time.astimezone(baghdad_tz)
        if match_baghdad.strftime('%Y-%m-%d') != today_date: continue
        match_timestamp = int(match_time.timestamp() * 1000)
        display_time = match_baghdad.strftime('%H:%M')
    except: continue

    league_id = match.get('competitionId')
    league_name = kurdish_leagues.get(league_id)
    if not league_name: continue

    channel_name = "پەخشی ڕاستەوخۆ"
    tv_networks = match.get('tvNetworks', [])
    if tv_networks:
        channel_name = tv_networks[0].get('name', 'beIN Sports')
    
    if channel_name == "پەخشی ڕاستەوخۆ" and league_id in [572, 7, 11, 25]:
        channel_name = "beIN Sports 📺"
    elif channel_name == "پەخشی ڕاستەوخۆ" and league_id == 6822:
        channel_name = "Al Iraqiya Sports 📺"

    home_team = match['homeCompetitor']['name']
    away_team = match['awayCompetitor']['name']
    home_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_96,h_96,c_limit,q_auto/v2/Competitors/{match['homeCompetitor']['id']}"
    away_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_96,h_96,c_limit,q_auto/v2/Competitors/{match['awayCompetitor']['id']}"
    
    stream_link = get_smart_stream_link(home_team, away_team)
    matches_added += 1

    if not stream_link or stream_link == "#":
        btn_html = f"""<button class="btn-disabled" disabled>لینک ئامادە نییە</button>"""
        has_link = "false"
    else:
        btn_html = f"""<button class="btn-live" onclick="openPlayer('{stream_link}', '{home_team} - {away_team}')">ڕاستەوخۆ 🔴</button>"""
        has_link = "true"

    html_content += f"""
        <div class="match-card" data-time="{match_timestamp}" data-haslink="{has_link}">
            <div class="league-badge">{league_name}</div>
            <div class="teams-wrapper">
                <div class="team"><img src="{home_logo}"><span>{home_team}</span></div>
                <div class="match-info">
                    <div class="match-time">{display_time}</div>
                    <div class="channel-tag" dir="ltr">{channel_name}</div>
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
    html_content += """
    <div style="text-align:center; margin-top: 50px; color: var(--text-sub);">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:15px; opacity:0.5;"><circle cx="12" cy="12" r="10"></circle><line x1="8" y1="12" x2="16" y2="12"></line></svg>
        <h3>هیچ یارییەکی گرنگ بۆ ئەمڕۆ نییە</h3>
    </div>
    """

html_content += """
    </div>

    <!-- شریتی خوارەوەی ئەپڵیکەیشن -->
    <div class="bottom-nav">
        <a href="#" class="nav-item active">
            <svg viewBox="0 0 24 24"><path d="M12 3L4 9v12h5v-7h6v7h5V9z"/></svg>
            <span>یارییەکان</span>
        </a>
        <a href="https://t.me/mtv_ibrahim_app" target="_blank" class="nav-item">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.97 1.25-5.56 3.67-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.06-.49-.83-.27-1.49-.41-1.43-.87.03-.24.36-.48 1-.74 3.92-1.7 6.54-2.83 7.86-3.38 3.74-1.56 4.51-1.83 5.02-1.84.11 0 .36.03.52.16.13.11.17.26.19.37.02.05.02.26.01.4z"/></svg>
            <span>تێلیگرام</span>
        </a>
        <a href="#" class="nav-item" onclick="alert('Kurd365 Live App\\nپەخشی ڕاستەوخۆی یارییەکان\\nگەشەپێدەر: ئیبراهیم')">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
            <span>دەربارە</span>
        </a>
    </div>

    <!-- پلەیەری ڕاستەوخۆ -->
    <div id="videoModal" class="modal">
        <div class="modal-header">
            <div class="modal-title" id="modalTitle" dir="ltr">Live Match</div>
            <button class="close-modal" onclick="closePlayer()">&times;</button>
        </div>
        <div class="modal-body">
            <iframe id="videoIframe" src="" allow="autoplay; encrypted-media; fullscreen" allowfullscreen="true" scrolling="no"></iframe>
        </div>
    </div>

    <script>
        function updateUI() {
            const now = new Date().getTime();
            document.querySelectorAll('.match-card').forEach(card => {
                const matchTime = parseInt(card.getAttribute('data-time'));
                const hasLink = card.getAttribute('data-haslink') === 'true';
                const diff = matchTime - now;
                
                const timerEl = card.querySelector('.countdown');
                const liveBtn = card.querySelector('.btn-live');
                const disabledBtn = card.querySelector('.btn-disabled');
                const finishedBtn = card.querySelector('.btn-finished');

                if (diff > 0) {
                    let h = Math.floor(diff / (1000 * 60 * 60));
                    let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diff % (1000 * 60)) / 1000);
                    timerEl.innerHTML = `⏳ ${h<10?'0'+h:h}:${m<10?'0'+m:m}:${s<10?'0'+s:s}`;
                    timerEl.style.display = 'inline-block'; 
                    if(liveBtn) liveBtn.style.display = 'none'; 
                    if(disabledBtn) disabledBtn.style.display = 'none';
                    finishedBtn.style.display = 'none';
                } else if (diff <= 0 && diff > -7200000) { 
                    timerEl.style.display = 'none'; 
                    finishedBtn.style.display = 'none'; 
                    if(hasLink && liveBtn) {
                        liveBtn.style.display = 'inline-block';
                        if(disabledBtn) disabledBtn.style.display = 'none';
                    } else if(disabledBtn) {
                        disabledBtn.style.display = 'inline-block';
                        if(liveBtn) liveBtn.style.display = 'none';
                    }
                } else {
                    timerEl.style.display = 'none'; 
                    if(liveBtn) liveBtn.style.display = 'none'; 
                    if(disabledBtn) disabledBtn.style.display = 'none';
                    finishedBtn.style.display = 'inline-block';
                }
            });
        }
        updateUI();
        setInterval(updateUI, 1000);

        const modal = document.getElementById('videoModal');
        const iframe = document.getElementById('videoIframe');
        const mTitle = document.getElementById('modalTitle');

        function openPlayer(link, title) {
            mTitle.innerText = title;
            iframe.src = link;
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function closePlayer() {
            modal.style.display = 'none';
            iframe.src = ""; 
            document.body.style.overflow = 'auto';
        }
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
