import requests
from bs4 import BeautifulSoup
from datetime import datetime

# زانیارییەکانی API-Football
api_key = "350fb25ebfcda5372357f8c8868450af" 
api_url = "https://v3.football.api-sports.io/fixtures"
today_date = datetime.today().strftime('%Y-%m-%d')

params = {
    "date": today_date,
    "timezone": "Asia/Baghdad"
}

headers = {
    'x-apisports-key': api_key
}

response = requests.get(api_url, headers=headers, params=params)
data = response.json()

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

# ئامادەکردنی بەشی سەرەوەی HTML لەگەڵ دیزاینە پڕۆفیشناڵەکە
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
        
        /* دیزاینی هێدەری Kurd365 */
        .header { background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 15px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header h1 { margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 1px; }
        
        .container { max-width: 700px; margin: 20px auto; padding: 0 10px; }
        
        /* دیزاینی خولەکان */
        .league-card { background: white; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); overflow: hidden; }
        .league-header { background-color: #ffffff; padding: 12px 15px; border-bottom: 2px solid #f0f2f5; display: flex; align-items: center; color: #2c3e50; font-weight: bold; font-size: 16px; }
        .league-header img { width: 25px; height: 25px; margin-left: 10px; }
        
        /* دیزاینی ڕیزی یارییەکان */
        .match-row { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #f9f9f9; }
        .match-row:last-child { border-bottom: none; }
        
        /* دیزاینی تیمەکان و لۆگۆکانیان */
        .team { display: flex; align-items: center; width: 35%; font-size: 14px; font-weight: 700; color: #333; }
        .team.away { justify-content: flex-end; }
        .team img { width: 30px; height: 30px; margin: 0 8px; }
        
        /* دیزاینی کات و ئەنجام */
        .match-center { width: 30%; text-align: center; display: flex; flex-direction: column; align-items: center; }
        .score-badge { background: #f0f2f5; padding: 4px 12px; border-radius: 20px; font-size: 15px; font-weight: bold; color: #1a1a1a; letter-spacing: 1px; direction: ltr; }
        .status-min { color: #e74c3c; font-size: 12px; font-weight: bold; margin-top: 4px; }
        
        /* دیزاینی دوگمەکان */
        .btn { margin-top: 8px; padding: 5px 12px; border-radius: 20px; text-decoration: none; color: white; font-size: 12px; font-weight: bold; transition: transform 0.2s; }
        .btn:hover { transform: scale(1.05); }
        .live { background: linear-gradient(45deg, #ff416c, #ff4b2b); box-shadow: 0 4px 10px rgba(255, 65, 108, 0.3); animation: pulse 1.5s infinite; }
        .upcoming { background-color: #3498db; }
        .finished { background-color: #95a5a6; pointer-events: none; }
        
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        
        /* گونجاندن بۆ شاشەی مۆبایل */
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

matches = data.get('response', [])
# ژمارە 542 بۆ خولی عێراقی زیادکراوە لێرەدا
important_leagues = [2, 3, 4, 39, 140, 135, 78, 61, 29, 542] 

# ڕێکخستن و جیاکردنەوەی یارییەکان بەپێی خولەکان
leagues_dict = {}
for match in matches:
    league_id = match['league']['id']
    if league_id in important_leagues:
        league_name = match['league']['name']
        if league_name not in leagues_dict:
            leagues_dict[league_name] = {
                'logo': match['league']['logo'],
                'matches': []
            }
        leagues_dict[league_name]['matches'].append(match)

if not leagues_dict:
    html_content += "<p style='text-align:center; padding: 20px; font-weight: bold;'>هیچ یارییەکی گرنگ لەم خولانەدا بۆ ئەمڕۆ نییە.</p>"
else:
    for league_name, league_data in leagues_dict.items():
        # دروستکردنی هێدەری خولەکە
        html_content += f"""
        <div class="league-card">
            <div class="league-header">
                <img src="{league_data['logo']}" alt="{league_name}">
                <span>{league_name}</span>
            </div>
        """
        
        for match in league_data['matches']:
            home_team = match['teams']['home']['name']
            home_logo = match['teams']['home']['logo']
            away_team = match['teams']['away']['name']
            away_logo = match['teams']['away']['logo']
            time = match['fixture']['date'][11:16] 
            status_short = match['fixture']['status']['short']
            
            goals_home = match['goals']['home'] if match['goals']['home'] is not None else "-"
            goals_away = match['goals']['away'] if match['goals']['away'] is not None else "-"
            
            stream_link = "#"
            status_text = ""
            
            if status_short in ['1H', '2H', 'HT', 'ET', 'P', 'BT']:
                btn_text = "ڕاستەوخۆ 🔴"
                btn_class = "live"
                score_display = f"{goals_home} - {goals_away}"
                status_text = f"{match['fixture']['status']['elapsed']}'"
                stream_link = get_stream_link(home_team, away_team)
            elif status_short in ['FT', 'AET', 'PEN']:
                btn_text = "تەواوبوو"
                btn_class = "finished"
                score_display = f"{goals_home} - {goals_away}"
            else:
                btn_text = "چاوەڕوانکراو"
                btn_class = "upcoming"
                score_display = time

            # دروستکردنی ڕیزی یارییەکە
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
        
        html_content += "</div>" # کۆتایی هاتنی دیڤی خولەکە

html_content += """
    </div>
</body>
</html>
"""

with open("live_matches.html", "w", encoding="utf-8") as file:
    file.write(html_content)
