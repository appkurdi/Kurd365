html_content = """<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kurd365 - خشتەی یارییەکان</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        body { font-family: 'Cairo', Tahoma, sans-serif; background-color: #f0f2f5; margin: 0; padding: 0; }
        
        /* هێدەری سەرەوەی Kurd365 */
        .header { background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 15px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header h1 { margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 1px; }
        
        .container { max-width: 700px; margin: 20px auto; padding: 0 10px; }
        
        /* دیزاینی دوگمەی پەخشی ڕاستەوخۆ */
        .stream-btn-container { text-align: center; margin: 25px 0; }
        .stream-btn {
            display: inline-block;
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            padding: 12px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4); }
            50% { transform: scale(1.05); box-shadow: 0 4px 20px rgba(255, 65, 108, 0.6); }
            100% { transform: scale(1); box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4); }
        }

        /* شاردنەوەی لۆگۆ و نوسینە زیادەکانی 365Scores بۆ ئەوەی پڕۆفیشناڵ بێت */
        #powered-by, .powered-by, [id^="powered-by"] { display: none !important; }
        
        /* بۆشایی نێوان خولەکان */
        .widget-wrapper { margin-bottom: 25px; border-radius: 12px; overflow: hidden; background: transparent; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Kurd365</h1>
    </div>
    <div class="container">
        
        <!-- دوگمەی چوون بۆ سێرڤەری پەخش -->
        <div class="stream-btn-container">
            <a href="https://syriashdab.com/" target="_blank" class="stream-btn">
                سەیرکردنی یارییەکان ڕاستەوخۆ 🔴
            </a>
        </div>

        <!-- خولی عێراقی -->
        <div class="widget-wrapper">
            <div data-widget-type="entityScores" data-entity-type="league" data-entity-id="6822" data-lang="ar" data-widget-id="0584ff28-08a8-43ee-a21e-604bb002689f"></div>
        </div>
        
        <!-- چامپیۆنزلیگ -->
        <div class="widget-wrapper">
            <div data-widget-type="entityScores" data-entity-type="league" data-entity-id="572" data-lang="ar" data-widget-id="0584ff28-08a8-43ee-a21e-604bb002689f"></div>
        </div>

        <!-- خولی ئینگلیزی -->
        <div class="widget-wrapper">
            <div data-widget-type="entityScores" data-entity-type="league" data-entity-id="7" data-lang="ar" data-widget-id="0584ff28-08a8-43ee-a21e-604bb002689f"></div>
        </div>

        <!-- خولی ئیسپانی -->
        <div class="widget-wrapper">
            <div data-widget-type="entityScores" data-entity-type="league" data-entity-id="11" data-lang="ar" data-widget-id="0584ff28-08a8-43ee-a21e-604bb002689f"></div>
        </div>

        <!-- خولی ئیتاڵی -->
        <div class="widget-wrapper">
            <div data-widget-type="entityScores" data-entity-type="league" data-entity-id="17" data-lang="ar" data-widget-id="0584ff28-08a8-43ee-a21e-604bb002689f"></div>
        </div>

        <!-- خولی ئەڵمانی -->
        <div class="widget-wrapper">
            <div data-widget-type="entityScores" data-entity-type="league" data-entity-id="25" data-lang="ar" data-widget-id="0584ff28-08a8-43ee-a21e-604bb002689f"></div>
        </div>

        <!-- خولی فەڕەنسی -->
        <div class="widget-wrapper">
            <div data-widget-type="entityScores" data-entity-type="league" data-entity-id="34" data-lang="ar" data-widget-id="0584ff28-08a8-43ee-a21e-604bb002689f"></div>
        </div>

    </div>

    <!-- سکریپتی سەرەکی 365Scores کە داتاکان دەهێنێت -->
    <script src="https://widgets.365scores.com/main.js"></script>
</body>
</html>"""

with open("live_matches.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("فایلی خشتەی یارییەکان بە سیستەمی ئایفرەیمی پڕۆفیشناڵ نوێ کرایەوە.")
