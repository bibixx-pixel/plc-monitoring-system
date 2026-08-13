## 📂PLC-MONITORING-SYSTEM 프로젝트 폴더 구조
- `root` : 파이썬 프로젝트의 최상위 폴더
  - `main.py`: 프로그램 진입점, 전체 프로그램 켜고 끄는 시작점. 프로그램이 켜지면 ui_event_manager 불러와 화면 켜달라는 명령 내리는 수준 정도로 구성.
  - `setup.py` : 빌드, 배포를 위해 필요한 설정

- `.gitignore` : git 커밋할 때 제외할 파일과 폴더 정의
- `README.md` : 프로젝트에 대한 설명을 포함한 파일, 일반적으로 프로젝트의 개요, 설치 방법, 사용법 등 포함
- `requirements.txt` : 해당 프로그램을 설치할 때 필요한 라이브러리

- `src/`: 핵심 소스코드 폴더
  - `__init__.py` : 폴더 안의 코드 불러오는 용도
  - `plc_worker.py`: PLC 통신 담당
  - `db_manager.py`: SQLite DB 관리
  - `devices.json` : PLC 주소(레지스터)를 설정할 수 있는 파일
  - `client.py` : 클라이언트 소켓 통신을 관리하는 파일

- `ui/`: 화면 디자인 폴더
  - `main_window.ui` : 디자인만 담당. Qt 디자이너로 그린 화면 디자인. 파이썬 코드 없음.
  - `ui_event_manager.py` : 사용자의 행동(버튼 클릭 등)을 담당. 디자인 파일 불러와 화면 출력. 화면 이벤트 연결 작업 처리.