import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# دیاریکردنی کاتی بەغدا (بۆ ئەوەی تەنها یارییەکانی ئەمڕۆی عێراق بهێنێت)
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

def get_stream_link(team_a_name, team_b_name):
    try:
        source_url = "https://syriashdab.com/"
        req = requests.get(source_url, timeout=10)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        for a_tag in soup.find_all('a', href=True):
            text = a_tag.text
            if team_a_name in text or team_b_name in text:
                link = a_tag['href']
                if not link.startswith('http'):
                    link = source_url.rstrip('/') + '/' + link.lstrip('/')
                return link
    except Exception as e:
        print(f"Error fetching stream: {e}")
    return "#"

html_content = """
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kurd365 - خشتەی یارییەکان</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        body { font-family: 'Cairo', Tahoma, sans-serif; background-color: #f0f2f5; margin: 0; padding: 0; }
        .header { background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 15px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header h1 { margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 1px; }
        .container { max-width: 700px; margin: 20px auto; padding: 0 10px; }
        .league-card { background: white; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); overflow: hidden; }
        .league-header { background-color: #ffffff; padding: 12px 15px; border-bottom: 2px solid #f0f2f5; display: flex; align-items: center; color: #2c3e50; font-weight: bold; font-size: 16px; }
        .league-header img { width: 25px; height: 25px; margin-left: 10px; }
        .match-row { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #f9f9f9; }
        .match-row:last-child { border-bottom: none; }
        .team { display: flex; align-items: center; width: 35%; font-size: 14px; font-weight: 700; color: #333; }
        .team.away { justify-content: flex-end; }
        .team img { width: 30px; height: 30px; margin: 0 8px; }
        .match-center { width: 30%; text-align: center; display: flex; flex-direction: column; align-items: center; }
        .score-badge { background: #f0f2f5; padding: 4px 12px; border-radius: 20px; font-size: 15px; font-weight: bold; color: #1a1a1a; letter-spacing: 1px; direction: ltr; }
        .status-min { color: #e74c3c; font-size: 12px; font-weight: bold; margin-top: 4px; }
        .btn { margin-top: 8px; padding: 5px 12px; border-radius: 20px; text-decoration: none; color: white; font-size: 12px; font-weight: bold; transition: transform 0.2s; }
        .btn:hover { transform: scale(1.05); }
        .live { background: linear-gradient(45deg, #ff416c, #ff4b2b); box-shadow: 0 4px 10px rgba(255, 65, 108, 0.3); animation: pulse 1.5s infinite; }
        .upcoming { background-color: #3498db; }
        .finished { background-color: #95a5a6; pointer-events: none; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        @media (max-width: 600px) {
            .team span { font-size: 12px; }
            .team img { width: 22px; height: 22px; }
            .score-badge { font-size: 14px; padding: 3px 8px; }
            .league-header { font-size: 14px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Kurd365</h1>
    </div>
    <div class="container">
"""

matches = data.get('games', [])
leagues_data_json = {comp['id']: comp for comp in data.get('competitions', [])}
leagues_dict = {}

kurdish_leagues = {
    6822: "خولی ئەستێرەکانی عێراق",
    572: "خولی یانە پاڵەوانەکانی ئەوروپا",
    7: "خولی ئینگلیزی (پریمەرلیگ)",
    11: "خولی ئیسپانی (لالیگا)",
    17: "خولی ئیتاڵی",
    25: "خولی ئەڵمانی",
    34: "خولی فەڕەنسی",
    573: "یۆرۆپالیگ"
}

for match in matches:
    # وەرگرتن و فلتەرکردنی کاتی یارییەکە بۆ ئەوەی تەنها یارییەکانی ئەمڕۆ بهێنێت
    start_time_str = match.get('startTime', '')
    try:
        match_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        match_baghdad = match_time.astimezone(baghdad_tz)
        match_date = match_baghdad.strftime('%Y-%m-%d')
        display_time = match_baghdad.strftime('%H:%M')
    except Exception as e:
        match_date = ""
        display_time = match.get('statusText', '')
        
    # ئەگەر یارییەکە بۆ ئەمڕۆ نەبوو، وازی لێ بهێنە و مەیهێنە ناو خشتەکەوە
    if match_date and match_date != today_date:
        continue

    league_id = match.get('competitionId')
    league_name = kurdish_leagues.get(league_id)
    if not league_name and league_id in leagues_data_json:
        league_name = leagues_data_json[league_id].get('name')
        
    if not league_name:
        continue

    if league_name not in leagues_dict:
        leagues_dict[league_name] = {
            'logo': f"https://imagecache.365scores.com/image/upload/f_auto,w_48,h_48,c_limit,q_auto/v2/Competitions/{league_id}",
            'matches': []
        }
    leagues_dict[league_name]['matches'].append(match)

if not leagues_dict:
    html_content += "<p style='text-align:center; padding: 20px; font-weight: bold;'>هیچ یارییەکی گرنگ لەم خولانەدا بۆ ئەمڕۆ نییە.</p>"
else:
    for league_name, league_data in leagues_dict.items():
        html_content += f"""
        <div class="league-card">
            <div class="league-header">
                <img src="{league_data['logo']}" alt="{league_name}">
                <span>{league_name}</span>
            </div>
        """
        
        for match in league_data['matches']:
            home_team = match['homeCompetitor']['name']
            home_id = match['homeCompetitor']['id']
            home_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_48,h_48,c_limit,q_auto/v2/Competitors/{home_id}"
            
            away_team = match['awayCompetitor']['name']
            away_id = match['awayCompetitor']['id']
            away_logo = f"https://imagecache.365scores.com/image/upload/f_auto,w_48,h_48,c_limit,q_auto/v2/Competitors/{away_id}"
            
            status_group = match.get('statusGroup', 1)
            
            # چارەسەری کێشەی (0.0) و گۆڕینی بۆ ژمارەی تەواو
            try:
                g_home = match['homeCompetitor'].get('score', -1)
                goals_home = str(int(g_home)) if g_home != -1 else "-"
            except:
                goals_home = "-"
                
            try:
                g_away = match['awayCompetitor'].get('score', -1)
                goals_away = str(int(g_away)) if g_away != -1 else "-"
            except:
                goals_away = "-"
            
            stream_link = "#"
            status_text = ""
            
            if status_group == 2:  # Live
                btn_text = "ڕاستەوخۆ 🔴"
                btn_class = "live"
                score_display = f"{goals_home} - {goals_away}"
                live_min = match.get('gameTimeDisplay', match.get('statusText', ''))
                status_text = f"{live_min}"
                stream_link = get_stream_link(home_team, away_team)
                
            elif status_group == 3:  # Finished
                btn_text = "تەواوبوو"
                btn_class = "finished"
                score_display = f"{goals_home} - {goals_away}"
                
            elif status_group == 4: # Postponed
                btn_text = "دواخرا"
                btn_class = "finished"
                score_display = "-"
                
            else:  # Scheduled (1)
                btn_text = "چاوەڕوانکراو"
                btn_class = "upcoming"
                score_display = display_time

            html_content += f"""
            <div class="match-row">
                <div class="team home">
                    <span>{home_team}</span>
                    <img src="{home_logo}" alt="{home_team}">
                </div>
                <div class="match-center">
                    <div class="score-badge">{score_display}</div>
                    {f"<div class='status-min'>{status_text}</div>" if status_text else ""}
                    <a href="{stream_link}" class="btn {btn_class}" target="_blank">{btn_text}</a>
                </div>
                <div class="team away">
                    <img src="{away_logo}" alt="{away_team}">
                    <span>{away_team}</span>
                </div>
            </div>
            """
        
        html_content += "</div>" 

html_content += """
    </div>
    
    <script>
        setInterval(function() {
            fetch(window.location.href, {cache: "no-store"})
            .then(response => response.text())
            .then(html => {
                var parser = new DOMParser();
                var doc = parser.parseFromString(html, 'text/html');
                var newContainer = doc.querySelector('.container');
                if (newContainer) {
                    document.querySelector('.container').innerHTML = newContainer.innerHTML;
                }
            })
            .catch(err => console.log("Error updating match data:", err));
        }, 60000);
    </script>
</body>
</html>
"""

with open("live_matches.html", "w", encoding="utf-8") as file:
    file.write(html_content)
