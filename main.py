import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# کاتی بەغدا
baghdad_tz = timezone(timedelta(hours=3))
today_date = datetime.now(baghdad_tz).strftime('%Y-%m-%d')

comps = "7,11,17,25,34,572,573,6822"
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

# فەنکشنی زۆر زیرەک بۆ هێنانی خودی ڤیدیۆی پەخشەکە بێ ڕیکلام
def get_smart_stream_link(team_a, team_b):
    try:
        base_url = "https://syriashdab.com/"
        req = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        # پاککردنەوە و دابەشکردنی ناوی یانەکان بۆ دۆزینەوەی ئاسانتر (نموونە: لابردنی 'نادي' و 'ال')
        ignore_words = ["نادي", "ال", "اف", "سي", "فريق"]
        words_a = [w for w in team_a.split() if len(w) > 2 and w not in ignore_words]
        words_b = [w for w in team_b.split() if len(w) > 2 and w not in ignore_words]
        
        match_page_url = ""
        
        # قۆناغی یەکەم: دۆزینەوەی لینکی یارییەکە لە پەڕەی سەرەکی
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
        
        # قۆناغی دووەم: چوونە ناو پەڕەی یارییەکە و دەرهێنانی تەنها ڤیدیۆکە (iframe)
        if match_page_url:
            page_req = requests.get(match_page_url, timeout=10)
            page_soup = BeautifulSoup(page_req.text, 'html.parser')
            
            iframes = page_soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src', '')
                # دوورکەوتنەوە لە ئایفرەیمی ڕیکلام و سۆشیاڵ میدیا
                if src and "facebook" not in src and "twitter" not in src and "youtube" not in src:
                    return src # ئەمە لینکی ڤیدیۆ ڕاستەقینەکەیە!
            
            return match_page_url # ئەگەر ئایفرەیمی نەدۆزیەوە، لینکی پەڕەکە خۆی دەگەڕێنێتەوە
            
    except Exception as e:
        pass
    return ""

html_content = """
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Kurd365 - پەخشی ڕاستەوخۆ</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
        
        :root {
            --primary-bg: #0d0d0d; --secondary-bg: #1a1a1c; --card-bg: #242426;
            --text-main: #ffffff; --text-muted: #8e8e93; --accent: #00f2fe;
            --live-btn: linear-gradient(135deg, #ff416c, #ff4b2b);
            --border-color: #38383a;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; margin: 0; padding: 0; }
        body { font-family: 'Cairo', sans-serif; background-color: var(--primary-bg); color: var(--text-main); padding-top: 70px; padding-bottom: 30px; }
        
        .navbar { position: fixed; top: 0; left: 0; width: 100%; height: 60px; z-index: 100; background: rgba(13, 13, 13, 0.9); backdrop-filter: blur(15px); display: flex; align-items: center; justify-content: center; border-bottom: 1px solid var(--border-color); }
        .navbar h1 { font-size: 24px; font-weight: 900; background: linear-gradient(135deg, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .container { max-width: 700px; margin: 0 auto; padding: 0 10px; }
        .page-title { font-size: 18px; font-weight: 800; margin: 10px 0 20px 0; text-align: center; color: var(--text-muted); }

        .match-card { background: var(--secondary-bg); border-radius: 16px; margin-bottom: 20px; border: 1px solid var(--border-color); overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.4); }
        .league-name { background: rgba(255,255,255,0.03); padding: 8px; font-size: 13px; font-weight: 700; color: var(--text-muted); text-align: center; border-bottom: 1px solid var(--border-color); }
        
        .teams-container { display: flex; justify-content: space-between; align-items: center; padding: 15px 10px; }
        .team { display: flex; flex-direction: column; align-items: center; width: 30%; gap: 8px; }
        .team img { width: 45px; height: 45px; }
        .team span { font-weight: 800; font-size: 12px; text-align: center; line-height: 1.3; }
        
        .match-center { width: 40%; display: flex; flex-direction: column; align-items: center; }
        .match-time { font-size: 22px; font-weight: 900; margin-bottom: 5px; }
        .tv-channel { font-size: 11px; background: rgba(0, 242, 254, 0.1); padding: 4px 10px; border-radius: 8px; color: var(--accent); font-weight: bold; border: 1px solid rgba(0, 242, 254, 0.2); text-align: center;}

        .status-footer { padding: 12px; background: rgba(0,0,0,0.3); border-top: 1px solid var(--border-color); text-align: center; min-height: 60px; display: flex; justify-content: center; align-items: center; }
        .countdown-timer { font-size: 15px; font-weight: 800; color: var(--accent); direction: ltr; display: none; }
        
        .stream-btn { display: none; background: var(--live-btn); color: white; padding: 8px 20px; border-radius: 30px; font-size: 14px; font-weight: 800; border: none; cursor: pointer; animation: pulse 1.5s infinite; }
        .stream-btn.disabled { background: #333; color: #888; animation: none; box-shadow: none; cursor: not-allowed; border: 1px solid #444; }
        .finished-btn { display: none; background: rgba(255, 255, 255, 0.1); color: #ccc; padding: 8px 25px; border-radius: 20px; font-size: 14px; font-weight: bold; border: 1px solid rgba(255,255,255,0.2); }

        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 65, 108, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(255, 65, 108, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 65, 108, 0); } }

        /* پلەیەر */
        #player-modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; display: none; flex-direction: column; }
        .player-header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: #111; border-bottom: 1px solid #222;}
        .player-title { color: white; font-weight: 800; font-size: 15px; }
        .close-btn { color: white; font-size: 28px; font-weight: bold; cursor: pointer; background: none; border: none; }
        .iframe-container { flex: 1; width: 100%; background: #000; position: relative; }
        .iframe-container iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>

    <div class="navbar"><h1>Kurd365</h1></div>
    <div class="container">
        <h2 class="page-title">خشتەی یارییەکانی ئەمڕۆ</h2>
"""

matches = data.get('games', [])
kurdish_leagues = {
    6822: "خولی عێراق", 572: "چامپیۆنزلیگ", 7: "پریمەرلیگ", 
    11: "لالیگا", 17: "خولی ئیتاڵی", 25: "خولی ئەڵمانی", 34: "خولی فەڕەنسی"
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

    # دۆزینەوەی ناوی کەناڵ زۆر بەوردی
    channel_name = "پەخشی ڕاستەوخۆ"
    tv_networks = match.get('tvNetworks', [])
    if tv_networks:
        channel_name = tv_networks[0].get('name', 'beIN Sports')
    
    # ئەگەر کەناڵەکەی نەزانی و خولەکە گەورە بوو، خۆی کەناڵی بۆ دادەنێت
    if channel_name == "پەخشی ڕاستەوخۆ" and league_id in [572, 7, 11, 34]:
        channel_name = "beIN Sports 📺"
    elif channel_name == "پەخشی ڕاستەوخۆ" and league_id == 6822:
        channel_name = "Al Iraqiya Sports 📺"

    home_team = match['homeCompetitor']['name']
    away_team = match['awayCompetitor']['name']
    home_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_96,h_96,c_limit,q_auto/v2/Competitors/{match['homeCompetitor']['id']}"
    away_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_96,h_96,c_limit,q_auto/v2/Competitors/{match['awayCompetitor']['id']}"
    
    # هێنانە دەرەوەی خودی پلەیەری ڤیدیۆکە
    stream_link = get_smart_stream_link(home_team, away_team)
    matches_added += 1

    if not stream_link or stream_link == "#":
        btn_html = f"""<button class="stream-btn disabled" disabled>لینک ئامادە نییە 🚫</button>"""
    else:
        btn_html = f"""<button class="stream-btn" onclick="openPlayer('{stream_link}', '{home_team} vs {away_team}')">سەیرکردنی ڕاستەوخۆ 🔴</button>"""

    html_content += f"""
        <div class="match-card" data-time="{match_timestamp}">
            <div class="league-name">{league_name}</div>
            <div class="teams-container">
                <div class="team"><img src="{home_logo}"><span>{home_team}</span></div>
                <div class="match-center">
                    <div class="match-time">{display_time}</div>
                    <div class="tv-channel" dir="ltr">{channel_name}</div>
                </div>
                <div class="team"><img src="{away_logo}"><span>{away_team}</span></div>
            </div>
            <div class="status-footer">
                <div class="countdown-timer"></div>
                {btn_html}
                <div class="finished-btn">یاری تەواوبوو</div>
            </div>
        </div>
    """

if matches_added == 0:
    html_content += "<p style='text-align:center; color: #888;'>هیچ یارییەکی گرنگ بۆ ئەمڕۆ نییە.</p>"

html_content += """
    </div>

    <div id="player-modal">
        <div class="player-header">
            <div class="player-title" id="player-title-text" dir="ltr">Live Match</div>
            <button class="close-btn" onclick="closePlayer()">×</button>
        </div>
        <div class="iframe-container">
            <!-- زیادکردنی تایبەتمەندی بۆ ئیشکردنی پلەیەر بەبێ کێشە -->
            <iframe id="video-iframe" src="" allow="autoplay; encrypted-media; fullscreen" allowfullscreen="true" scrolling="no"></iframe>
        </div>
    </div>

    <script>
        function updateCountdowns() {
            const now = new Date().getTime();
            document.querySelectorAll('.match-card').forEach(card => {
                const matchTime = parseInt(card.getAttribute('data-time'));
                const diff = matchTime - now;
                
                const timerEl = card.querySelector('.countdown-timer');
                const streamBtn = card.querySelector('.stream-btn');
                const finishedBtn = card.querySelector('.finished-btn');

                if (diff > 0) {
                    let h = Math.floor(diff / (1000 * 60 * 60));
                    let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diff % (1000 * 60)) / 1000);
                    timerEl.innerHTML = `کاتی ماوە: ${h<10?'0'+h:h}:${m<10?'0'+m:m}:${s<10?'0'+s:s}`;
                    timerEl.style.display = 'block'; 
                    if(streamBtn) streamBtn.style.display = 'none'; 
                    finishedBtn.style.display = 'none';
                } else if (diff <= 0 && diff > -7200000) { 
                    timerEl.style.display = 'none'; 
                    finishedBtn.style.display = 'none'; 
                    if(streamBtn) streamBtn.style.display = 'inline-block';
                } else {
                    timerEl.style.display = 'none'; 
                    if(streamBtn) streamBtn.style.display = 'none'; 
                    finishedBtn.style.display = 'inline-block';
                }
            });
        }
        updateCountdowns();
        setInterval(updateCountdowns, 1000);

        const modal = document.getElementById('player-modal');
        const iframe = document.getElementById('video-iframe');
        const titleText = document.getElementById('player-title-text');

        function openPlayer(link, title) {
            titleText.innerText = title;
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
