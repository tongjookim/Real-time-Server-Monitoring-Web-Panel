# 🛡️ Real-time Server Sentinel (Olive Dashboard)

![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-v3.0-green?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-important)

> **상용 수준의 비주얼과 안정성을 갖춘 경량 실시간 서버 모니터링 웹 패널입니다.** > A professional-grade, lightweight real-time server monitoring dashboard with a sleek Olive-Dark theme.

---

## 📸 Preview
![Dashboard Preview](https://sir.kr/storage/showcases/2026/04/nBlvC8aPkzBfg1OdWxpL.jpg)
*실제 구동 중인 대시보드의 모습입니다. 독보적인 Olive 테마로 시인성을 높였습니다.*

---

## ✨ Key Features (주요 기능)

### 🖥️ System Resources Monitoring
- **Real-time Metrics**: CPU, RAM, Disk 사용량을 실시간 퍼센트로 표시합니다.
- **Dynamic Graphs**: Chart.js를 활용하여 리소스 변화 추이를 부드러운 선 그래프로 시각화합니다.

### 🌐 Network Traffic Analysis
- **Live Speed**: 현재 서버의 업로드 및 다운로드 속도를 실시간으로 측정합니다.
- **Accumulated Stats**: 일간, 주간, 월간, 연간 누적 트래픽을 계산하여 효율적인 대역폭 관리를 돕습니다.

### 🔗 Active Connection Viewer
- **Connection Mapping**: 현재 서버에 연결된 모든 활성 세션의 로컬 IP와 외부 IP를 매핑하여 보여줍니다.
- **Stability**: `psutil` 라이브러리의 `raddr`(Remote Address) 예외 처리를 통해 리스닝 포트나 로컬 소켓에서도 에러 없이 안정적으로 작동합니다.

### 🎨 Premium UI/UX
- **Olive-Dark Theme**: 장시간 관제 시 눈의 피로도를 줄여주는 다크 그린 계열의 커스텀 테마를 적용했습니다.
- **Responsive Design**: 다양한 화면 크기에서도 대시보드 레이아웃이 깨지지 않도록 설계되었습니다.

---

## 🛠️ Tech Stack (기술 스택)

| Category | Technology |
| :--- | :--- |
| **Backend** | Python 3.10, Flask |
| **Data Collection** | psutil |
| **Frontend** | HTML5, CSS3, Vanilla JS |
| **Chart Library** | Chart.js |
| **Environment** | Linux (Ubuntu), SSH |

---

## 🚀 Installation & Setup (설치 방법)

### 1. Requirements
서버에 `tar`, `wget`, `curl`이 설치되어 있어야 하며, Python 환경이 필요합니다.

### 2. Clone Repository
```bash
git clone [https://github.com/tongjookim/Real-time-Server-Monitoring-Web-Panel.git](https://github.com/tongjookim/Real-time-Server-Monitoring-Web-Panel.git)
cd Real-time-Server-Monitoring-Web-Panel
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python app.py
```
브라우저에서 http://your-server-ip:5000으로 접속하세요.

## 📂 Project Structure
```
├── app.py              # Flask 백엔드 로직 및 데이터 수집 (psutil)
├── static/
│   ├── css/            # Olive 테마 커스텀 스타일시트
│   └── js/             # Chart.js 연동 및 실시간 데이터 업데이트 로직
├── templates/
│   └── index.html      # 메인 대시보드 구조
└── requirements.txt    # 의존성 패키지 목록
```

## 🔒 Technical Note & Security
- raddr Exception Handling: 네트워크 연결 조회 시 raddr 속성이 없는 경우(Listen 상태 등)를 대비한 예외 처리가 적용되어 있어 서버 다운 타임을 방지합니다.
- Security Warning: 깃허브에 푸시할 때 SSH 키 파일(id_rsa)이나 서버 설정 파일이 포함되지 않도록 .gitignore 설정을 반드시 확인하세요.

## 📄 License
이 프로젝트는 MIT License를 따릅니다. 개인적/상업적 용도로 자유롭게 수정 및 배포가 가능합니다.
