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

# فانکشنی سکراپینگ بۆ دۆزینەوەی لینکی یارییەکە
def get_stream_link(team_a_name, team_b_name):
    try:
        # سەردانیکردنی ماڵپەڕی سەرچاوە
        source_url = "https://syriashdab.com/"
        req = requests.get(source_url, timeout=10)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        # گەڕان بەناو هەموو لینکەکانی ماڵپەڕەکەدا
        for a_tag in soup.find_all('a', href=True):
            text = a_tag.text
            # ئەگەر ناوی یەکێک لە تیمەکانی تێدابوو، لینکەکەی بهێنە
            if team_a_name in text or team_b_name in text:
                link = a_tag['href']
                # دڵنیابوونەوە لەوەی لینکەکە تەواوە
                if not link.startswith('http'):
                    link = source_url.rstrip('/') + '/' + link.lstrip('/')
                return link
    except Exception as e:
        print(f"Error fetching stream: {e}")
    
    return "#" # ئەگەر نەیدۆزیەوە یان کێشەیەک هەبوو

# ئامادەکردنی بەشی سەرەوەی HTML
html_content = """
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>خشتەی یارییەکانی ئەمڕۆ</title>
    <style>
        body { font-family: Tahoma, Arial, sans-serif; background-color: #f4f4f9; padding: 15px; margin: 0; }
        .matches-container { max-width: 600px; margin: 0 auto; }
        .match-card { background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; text-align: center; }
        .team { font-size: 15px; font-weight: bold; width: 30%; color: #333; }
        .time-score { font-size: 14px; color: #555; width: 20%; direction: ltr; font-weight: bold; }
        .btn { padding: 8px 12px; border-radius: 5px; text-decoration: none; color: white; font-weight: bold; font-size: 13px; }
        .live { background-color: #e74c3c; animation: pulse 1.5s infinite; }
        .upcoming { background-color: #f39c12; }
        .finished { background-color: #95a5a6; pointer-events: none; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        h2 { text-align: center; color: #2c3e50; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="matches-container">
        <h2>یارییەکانی ئەمڕۆ</h2>
"""

matches = data.get('response', [])
important_leagues = [2, 3, 4, 39, 140, 135, 78, 61, 29] 
filtered_matches = [m for m in matches if m['league']['id'] in important_leagues]

if not filtered_matches:
    html_content += "<p style='text-align:center;'>هیچ یارییەکی گرنگ لەم خولانەدا بۆ ئەمڕۆ نییە.</p>"
else:
    for match in filtered_matches:
        team_a = match['teams']['home']['name']
        team_b = match['teams']['away']['name']
        time = match['fixture']['date'][11:16] 
        status_short = match['fixture']['status']['short']
        
        goals_home = match['goals']['home'] if match['goals']['home'] is not None else "-"
        goals_away = match['goals']['away'] if match['goals']['away'] is not None else "-"
        
        stream_link = "#"
        
        if status_short in ['1H', '2H', 'HT', 'ET', 'P', 'BT']:
            btn_text = "سەیرکردن 🔴"
            btn_class = "live"
            display_time = f"{goals_home} - {goals_away}<br><span style='color:red;font-size:12px;'>{match['fixture']['status']['elapsed']}'</span>"
            
            # لە کاتی یارییەکەدا، بگەڕێ بەدوای لینکەکەدا
            stream_link = get_stream_link(team_a, team_b)
            
        elif status_short in ['FT', 'AET', 'PEN']:
            btn_text = "تەواوبوو 🏁"
            btn_class = "finished"
            display_time = f"{goals_home} - {goals_away}"
        else:
            btn_text = "چاوەڕوانکراو ⏳"
            btn_class = "upcoming"
            display_time = time

        html_content += f"""
            <div class="match-card">
                <div class="team">{team_a}</div>
                <div class="time-score">{display_time}</div>
                <div class="team">{team_b}</div>
                <!-- کردنەوەی لینکەکە لە پەنجەرەیەکی نوێدا ئەگەر دۆزرایەوە -->
                <a href="{stream_link}" class="btn {btn_class}" target="_blank">{btn_text}</a>
            </div>
        """

html_content += """
    </div>
</body>
</html>
"""

with open("live_matches.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("فایلی خشتەی یارییەکان بە سەرکەوتوویی لەگەڵ لینکەکان دروستکرا.")
