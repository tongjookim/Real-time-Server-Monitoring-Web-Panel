from flask import Flask, render_template, jsonify, session, request, redirect, url_for, flash
import psutil
import time
import datetime
import os
import secrets
import threading
import json
from pathlib import Path
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key')

PANEL_USERNAME = os.getenv('PANEL_USERNAME', 'admin')
PANEL_PASSWORD = os.getenv('PANEL_PASSWORD', 'admin')

# 네트워크 속도 계산을 위한 글로벌 변수
last_net_io = psutil.net_io_counters()
last_time = time.time()

# 트래픽 로그 파일 경로
TRAFFIC_LOG_PATH = Path(__file__).parent / 'traffic_log.json'
traffic_log_lock = threading.Lock()

# ── 트래픽 로그 유틸 ──────────────────────────────────────────

def load_traffic_log():
    if TRAFFIC_LOG_PATH.exists():
        with open(TRAFFIC_LOG_PATH, 'r') as f:
            return json.load(f)
    return {"daily": {}}

def save_traffic_log(log):
    with open(TRAFFIC_LOG_PATH, 'w') as f:
        json.dump(log, f)

def record_traffic(sent_bytes, recv_bytes):
    today = datetime.date.today().isoformat()
    with traffic_log_lock:
        log = load_traffic_log()
        day = log['daily'].setdefault(today, {'sent': 0, 'recv': 0})
        day['sent'] += sent_bytes
        day['recv'] += recv_bytes
        save_traffic_log(log)

def aggregate_traffic(days):
    today = datetime.date.today()
    with traffic_log_lock:
        log = load_traffic_log()
    daily = log.get('daily', {})
    total_sent = total_recv = 0
    for i in range(days):
        key = (today - datetime.timedelta(days=i)).isoformat()
        if key in daily:
            total_sent += daily[key]['sent']
            total_recv += daily[key]['recv']
    return total_sent, total_recv

# ── 백그라운드 트래픽 샘플러 (60초 간격) ─────────────────────

def traffic_sampler():
    last_io = psutil.net_io_counters()
    while True:
        time.sleep(60)
        current_io = psutil.net_io_counters()
        sent = max(0, current_io.bytes_sent - last_io.bytes_sent)
        recv = max(0, current_io.bytes_recv - last_io.bytes_recv)
        last_io = current_io
        record_traffic(sent, recv)

threading.Thread(target=traffic_sampler, daemon=True).start()

# ── 인증 ─────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user_ok = secrets.compare_digest(username, PANEL_USERNAME)
        pass_ok = secrets.compare_digest(password, PANEL_PASSWORD)
        if user_ok and pass_ok:
            session['logged_in'] = True
            return redirect(url_for('index'))
        flash('아이디 또는 비밀번호가 올바르지 않습니다.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── 페이지 ────────────────────────────────────────────────────

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# ── API ──────────────────────────────────────────────────────

@app.route('/api/stats')
@login_required
def stats():
    global last_net_io, last_time

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    interval = current_time - last_time if current_time > last_time else 1

    up_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / interval / 1024 / 1024
    down_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / interval / 1024 / 1024

    last_net_io = current_net_io
    last_time = current_time

    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.raddr:
            connections.append({
                'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                'remote': f"{conn.raddr.ip}:{conn.raddr.port}",
                'status': conn.status
            })

    return jsonify({
        'cpu': cpu,
        'ram': ram,
        'disk': disk,
        'up': round(up_speed, 2),
        'down': round(down_speed, 2),
        'conns': connections[:10],
        'uptime': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/traffic')
@login_required
def traffic():
    def to_unit(b):
        gb = b / 1024 ** 3
        if gb >= 1:
            return f"{gb:.2f} GB"
        mb = b / 1024 ** 2
        if mb >= 1:
            return f"{mb:.1f} MB"
        return f"{b / 1024:.1f} KB"

    periods = {
        'daily':   1,
        'weekly':  7,
        'monthly': 30,
        'annual':  365,
    }
    result = {}
    for key, days in periods.items():
        sent, recv = aggregate_traffic(days)
        result[key] = {
            'sent': to_unit(sent),
            'recv': to_unit(recv),
            'total': to_unit(sent + recv),
        }
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8650, debug=False)
