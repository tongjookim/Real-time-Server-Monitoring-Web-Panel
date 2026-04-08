# My Server Monitor
- 목적: 본 프로젝트는 중소규모 서버 환경에서 실시간 트래픽 과부하를 감시하고, 시스템 핵심 자원(CPU, RAM, Disk)을 모니터링하기 위해 구축된 경량 웹 패널입니다. cPanel 등의 상용 솔루션 비용 부담을 줄이면서도 실질적인 트래픽 원인 분석 기능을 제공하는 것을 목표로 합니다.
- 스택: Python, Flask, psutil, Bootstrap 5
- 주요 기능: 
  - 실시간 시스템 모니터링: CPU, 메모리, 디스크 사용량을 2초 간격으로 시각화
  - 네트워크 대역폭 추적: 현재 업로드 및 다운로드 속도를 MB/s 단위로 실시간 계산
  - 활성 연결 감시(Active Connections): 서버에 연결된 외부 IP와 포트 정보를 실시간 리스트업하여 트래픽 유발원을 특정.
- 주요 보안 사항: 특정 포트(8650) 사용, SSH 터널링 권장
- 파일 구조:
 * app.py: Flask 기반의 API 및 웹 서버.
 * templates/index.html: 실시간 대시보드 UI 템플릿.
 * requirements.txt: 프로젝트 의존성 라이브러리 목록.
-  Claude Code 유지보수 가이드 (Maintenance Note)
 1. psutil의 raddr 속성 체크 (필수):
  * psutil.net_connections() 호출 시, 특정 연결 타입에서 원격 주소 정보(raddr)가 누락되어 AttributeError가 발생할 수 있습니다.
  * 반드시 if conn.raddr: 조건문을 통해 해당 속성이 존재하는지 확인한 후 ip 및 port에 접근해야 합니다.

 2. 트래픽 속도 계산 로직:
  * 속도는 psutil.net_io_counters()의 누적값 차이를 시간 간격(interval)으로 나누어 계산합니다.
  * last_net_io와 last_time 글로벌 변수의 업데이트 주기가 어긋나지 않도록 주의해야 합니다.

 3. 보안 준수
  * 본 패널은 관리용 도구이므로 외부에 노출되어서는 안 됩니다.
  * 운영 환경에서는 반드시 UFW 방화벽을 설정하여 허용된 IP에서만 접속하게 하거나, SSH 터널링을 통해 접근하도록 유도하십시오.

- 향후 로드맵
 * [ ] Flask-HTTPAuth를 활용한 간단한 관리자 로그인 기능.
 * [ ] Chart.js를 사용한 최근 1시간 트래픽 변동 추이 그래프.
 * [ ] 트래픽 과다 유발 IP를 원클릭으로 ufw 차단하는 기능.
 * [ ] 특정 트래픽 임계치 도달 시 텔레그램 봇 자동 알림.
