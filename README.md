# 🚀 창업 리포트 차트 API 서버

**FE에서 차트 사양을 가져올 수 있는 REST API를 제공합니다.**

> 🎯 **목적**: 프론트엔드 개발자가 차트 라이브러리별 사양(spec)을 쉽게 가져와서 차트를 렌더링할 수 있도록 지원

## 📋 목차

- [✨ 주요 기능](#-주요-기능)
- [📊 제공하는 차트](#-제공하는-차트)
- [🛠️ 지원하는 차트 라이브러리](#️-지원하는-차트-라이브러리)
- [🚀 빠른 시작](#-빠른-시작)
- [🐳 Docker 사용법](#-docker-사용법)
- [📡 API 엔드포인트](#-api-엔드포인트)
- [📚 API 문서](#-api-문서)
- [🔧 사용 예시](#-사용-예시)
- [🧪 테스트](#-테스트)
- [✅ 코드 품질](#-코드-품질)
- [🎨 프론트엔드 개발자 가이드](#-프론트엔드-개발자-가이드)
- [🛠️ 개발 및 배포](#️-개발-및-배포)
- [🔧 문제 해결](#-문제-해결)
- [🤝 기여하기](#-기여하기)

## ✨ 주요 기능

- 🎨 **4가지 차트 라이브러리 지원**: Vega-Lite, ECharts, Plotly, Chart.js
- 📊 **실시간 데이터 로드**: CSV 파일에서 동적으로 차트 데이터 로드
- 🔍 **완벽한 API 문서화**: Swagger UI + ReDoc 제공
- 🚀 **RESTful API**: 표준 HTTP 메서드와 상태 코드 사용
- 🌐 **CORS 지원**: 크로스 오리진 요청 허용
- 🐳 **Docker 지원**: 프로덕션/개발 환경 컨테이너화
- 🔄 **CI/CD 파이프라인**: GitHub Actions 자동화
- ✅ **코드 품질 관리**: Black, isort, flake8, pre-commit hooks
- 🧪 **테스트 커버리지**: pytest, 자동화된 API 테스트
- 🔧 **핫 리로드**: 개발 환경에서 코드 변경 시 자동 재시작

## 📊 제공하는 차트

### 1. 연도별 업종별 총 가맹점수 추이 (라인 차트)
- **설명**: 2017년~2024년 동안 도소매, 서비스, 외식 업종의 총 가맹점수 변화 추이
- **차트 타입**: 라인 차트 (점 마커 포함)

### 2. 업종별 전체 기간 평균 가맹점수 (바 차트)
- **설명**: 전체 기간 동안의 업종별 평균 가맹점수 비교
- **차트 타입**: 바 차트

## 🛠️ 지원하는 차트 라이브러리

- **Vega-Lite**: 선언적 차트 라이브러리
- **ECharts**: 강력한 JavaScript 차트 라이브러리
- **Plotly**: Python 기반 인터랙티브 차트
- **Chart.js**: 간단하고 유연한 JavaScript 차트

## 🚀 빠른 시작

### 설치

#### Git에서 직접 설치
```bash
# 프로젝트 클론
git clone https://github.com/LEEYH205/startup_report_api.git
cd startup_report_api
```

#### 로컬에서 설치
```bash
# 프로젝트 클론
git clone https://github.com/LEEYH205/startup_report_api.git
cd startup_report_api

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 데이터 설정

#### 🗂️ **팀 공유 데이터**
프로젝트에 필요한 데이터 파일들이 Google Drive에 저장되어 있습니다.

**📥 데이터 다운로드:**
1. [팀 공유 Google Drive 폴더](https://drive.google.com/drive/folders/1exJ1ppaVf-_7vsRTqNgsBdB5PB4THjoW?usp=sharing)에 접속
2. 모든 CSV 파일을 다운로드
3. 프로젝트 루트에 `data/` 폴더 생성
4. 다운로드한 파일들을 `data/` 폴더에 복사

**📁 필요한 파일들:**
- `지역별_도소매별_가맹점수_현황.csv`
- `지역별_서비스별_가맹점수_현황.csv`
- `지역별_외식별_가맹점수_현황.csv`

```bash
# 파일 구조 확인
ls data/
# 출력되어야 할 파일들:
# 지역별_도소매별_가맹점수_현황.csv
# 지역별_서비스별_가맹점수_현황.csv
# 지역별_외식별_가맹점수_현황.csv
```

### API 서버 실행
```bash
# 가상환경이 활성화되어 있는지 확인
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 기본 포트(5001)로 실행
python app.py

# 특정 포트로 실행
python app.py --port 8080

# 특정 호스트와 포트로 실행
python app.py --host 0.0.0.0 --port 8000

# 디버그 모드로 실행
python app.py --debug

# 또는 실행 스크립트 사용
./run_server.sh

# 자동 설정 스크립트 실행 (권장)
./setup_and_test.sh
```

서버가 `http://localhost:5001`에서 실행됩니다.

### API 테스트
```bash
# 가상환경이 활성화되어 있는지 확인
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# API 테스트
python test_api_client.py
```

## 🐳 Docker 사용법

### Docker 이미지 빌드 및 실행

#### 1. 기본 Docker 사용
```bash
# Docker 이미지 빌드
./docker-build.sh build

# Docker 컨테이너 실행
./docker-build.sh run

# Docker 컨테이너 중지
./docker-build.sh stop

# Docker 컨테이너 로그 확인
./docker-build.sh logs

# Docker 컨테이너 테스트
./docker-build.sh test

# Docker 정리
./docker-build.sh clean
```

#### 2. Docker Compose 사용 (개발 환경)
```bash
# 개발 환경 시작 (핫 리로드)
./docker-compose-dev.sh up

# 개발 환경 중지
./docker-compose-dev.sh down

# 개발 환경 재시작
./docker-compose-dev.sh restart

# 로그 확인
./docker-compose-dev.sh logs

# API 테스트
./docker-compose-dev.sh test

# 상태 확인
./docker-compose-dev.sh status
```

#### 3. 직접 Docker 명령어 사용
```bash
# 프로덕션 이미지 빌드
docker build -t chart-api-server:latest .

# 개발용 이미지 빌드
docker build -t chart-api-server:dev -f Dockerfile.dev .

# 프로덕션 컨테이너 실행
docker run -d \
  --name chart-api-server \
  -p 5001:5001 \
  -v "$(pwd)/data:/app/data:ro" \
  -v "$(pwd)/chart_specs_json:/app/chart_specs_json:ro" \
  chart-api-server:latest

# 개발용 컨테이너 실행 (핫 리로드)
docker run -d \
  --name chart-api-server-dev \
  -p 5002:5001 \
  -v "$(pwd):/app" \
  -v "$(pwd)/data:/app/data:ro" \
  -v "$(pwd)/chart_specs_json:/app/chart_specs_json:ro" \
  chart-api-server:dev
```

### Docker Compose 환경
```bash
# 모든 서비스 시작
docker-compose up -d

# 개발 환경만 시작
docker-compose --profile dev up -d

# 서비스 중지
docker-compose down

# 로그 확인
docker-compose logs -f
```

## 📡 API 엔드포인트

### 기본 정보
- **GET /** - API 루트 및 사용 가능한 엔드포인트 정보
- **GET /health** - 서버 상태 확인

### 차트 사양 API
- **GET /api/charts** - 모든 차트 라이브러리의 모든 차트 사양
- **GET /api/charts/{library}** - 특정 라이브러리의 모든 차트 사양
- **GET /api/charts/{library}/{type}** - 특정 라이브러리의 특정 차트 타입 사양

### 데이터 API
- **GET /api/data** - 원본 차트 데이터

## 📚 API 문서

### Swagger UI
- **URL**: http://localhost:5001/docs
- **설명**: 인터랙티브한 API 문서 및 테스트 도구
- **기능**: API 엔드포인트 테스트, 요청/응답 스키마 확인, 실시간 API 호출

### ReDoc
- **URL**: http://localhost:5001/redoc
- **설명**: 깔끔하고 읽기 쉬운 API 문서
- **기능**: 직관적인 API 문서 탐색, 응답 모델 상세 정보

## 🔧 사용 예시

### 모든 차트 사양 가져오기
```bash
curl http://localhost:5001/api/charts/
```

### ECharts 라인 차트 사양만 가져오기
```bash
curl http://localhost:5001/api/charts/echarts/line
```

### 특정 라이브러리의 모든 차트 가져오기
```bash
curl http://localhost:5001/api/charts/vega_lite
curl http://localhost:5001/api/charts/plotly
curl http://localhost:5001/api/charts/chartjs
```

### 원본 데이터 가져오기
```bash
curl http://localhost:5001/api/data/
curl http://localhost:5001/api/data/?type=line
curl http://localhost:5001/api/data/?type=bar
```

## 🧪 테스트

### 자동화된 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 테스트 실행
pytest --cov=. --cov-report=html

# 특정 테스트 파일 실행
pytest tests/test_api.py -v

# API 테스트만 실행
python test_api_client.py
```

### Docker 환경에서 테스트
```bash
# 개발 환경에서 API 테스트
./docker-compose-dev.sh test

# 프로덕션 환경에서 API 테스트
./docker-build.sh test
```

### 테스트 종류
- **API 테스트**: 모든 엔드포인트의 정상 작동 확인
- **차트 사양 테스트**: 각 차트 라이브러리별 사양 유효성 검증
- **데이터 로드 테스트**: CSV 파일 로드 및 데이터 처리 확인
- **헬스체크 테스트**: 서버 상태 및 의존성 확인

## ✅ 코드 품질

### 자동 포맷팅 및 검사
```bash
# 코드 포맷팅 (Black)
black .

# Import 정렬 (isort)
isort . --profile=black

# 코드 품질 검사 (flake8)
flake8 . --max-line-length=88 --extend-ignore=E203

# 모든 검사 한 번에 실행
black . && isort . --profile=black && flake8 . --max-line-length=88 --extend-ignore=E203
```

### Pre-commit Hooks
```bash
# Pre-commit hooks 설치
pre-commit install

# 모든 파일에 대해 pre-commit 실행
pre-commit run --all-files

# 특정 hook만 실행
pre-commit run black
pre-commit run isort
pre-commit run flake8
```

### VS Code 설정
`.vscode/settings.json`에서 자동 포맷팅이 설정되어 있습니다:
- **저장 시 자동 포맷팅**: Black 사용
- **저장 시 import 정리**: isort 사용
- **실시간 linting**: flake8 사용

### 코드 품질 도구
- **Black**: 일관된 코드 포맷팅
- **isort**: import 문 자동 정렬
- **flake8**: PEP8 준수 및 코드 품질 검사
- **pre-commit**: Git commit 전 자동 검사

## 🛠️ 개발 및 배포

### 개발 모드
```bash
# 개발 서버 실행 (자동 재시작, 디버그 모드)
python app.py

# 또는 환경변수 설정
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py

# Docker 개발 환경 사용 (권장)
./docker-compose-dev.sh up
```

### 프로덕션 배포
```bash
# Gunicorn 사용 (권장)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app

# 또는 uWSGI 사용
pip install uwsgi
uwsgi --http :5001 --wsgi-file app.py --callable app

# Docker 프로덕션 환경 사용 (권장)
./docker-build.sh build
./docker-build.sh run
```

### CI/CD 파이프라인
이 프로젝트는 GitHub Actions를 사용한 완전 자동화된 CI/CD 파이프라인을 포함합니다:

#### 🔄 자동화된 워크플로우
1. **코드 품질 검사** (`code-quality`)
   - Black 코드 포맷팅 검사
   - isort import 정렬 검사
   - flake8 코드 품질 검사

2. **테스트 실행** (`test`)
   - Python 3.11에서 모든 테스트 실행
   - 커버리지 측정 및 리포트 생성
   - Codecov 업로드

3. **Docker 빌드 및 테스트** (`docker-build`)
   - 프로덕션 Docker 이미지 빌드
   - 개발용 Docker 이미지 빌드
   - 각 이미지의 헬스체크 테스트

4. **보안 스캔** (`security-scan`)
   - 기본 보안 검사 실행
   - 의존성 취약점 확인

5. **배포 알림** (`deploy-notification`)
   - 모든 단계 완료 시 성공 알림

#### 🚀 트리거 조건
- **Push**: `main`, `develop` 브랜치
- **Pull Request**: `main`, `develop` 브랜치 대상
- **자동 배포**: `main` 브랜치 푸시 시에만 실행

## 🎨 프론트엔드 개발자 가이드

### 1. 차트 사양 가져오기
```javascript
// 모든 차트 사양 가져오기
const response = await fetch('http://localhost:5001/api/charts/');
const allCharts = await response.json();

// ECharts 라인 차트 사양 가져오기
const lineChartResponse = await fetch('http://localhost:5001/api/charts/echarts/line');
const lineChartSpec = await lineChartResponse.json();
```

### 2. 차트 렌더링 예시

#### ECharts 사용
```javascript
import * as echarts from 'echarts';

// 차트 사양 가져오기
const response = await fetch('http://localhost:5001/api/charts/echarts/line');
const option = await response.json();

// 차트 렌더링
const chart = echarts.init(document.getElementById('chart-container'));
chart.setOption(option);
```

#### Vega-Lite 사용
```javascript
import { embed } from 'vega-embed';

// 차트 사양 가져오기
const response = await fetch('http://localhost:5001/api/charts/vega_lite/line');
const spec = await response.json();

// 차트 렌더링
await embed('#chart-container', spec);
```

#### Chart.js 사용
```javascript
import Chart from 'chart.js/auto';

// 차트 사양 가져오기
const response = await fetch('http://localhost:5001/api/charts/chartjs/line');
const config = await response.json();

// 차트 렌더링
new Chart(document.getElementById('chart-canvas'), config);
```

## 🔧 문제 해결

### 일반적인 문제들

#### 1. 포트 충돌
```bash
# 포트 5001이 이미 사용 중인 경우
lsof -i :5001
kill -9 <PID>

# 또는 다른 포트 사용
python app.py --port 5002
```

#### 2. 가상환경 문제
```bash
# 가상환경 재생성
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 3. CSV 파일 로드 실패
```bash
# 데이터 폴더 확인
ls -la data/
# CSV 파일 권한 확인
chmod 644 data/*.csv
```

#### 4. Docker 관련 문제
```bash
# Docker 컨테이너 상태 확인
docker ps -a

# Docker 로그 확인
docker logs chart-api-server

# Docker 컨테이너 재시작
docker restart chart-api-server

# Docker 이미지 재빌드
./docker-build.sh build
```

### 로그 확인
```bash
# Flask 디버그 로그 활성화
export FLASK_DEBUG=1
python app.py

# 또는 로그 파일로 출력
python app.py > app.log 2>&1

# Docker 로그 확인
./docker-build.sh logs
```

## 🤝 기여하기

### 개발 환경 설정
1. 이 저장소를 포크합니다
2. 로컬에 클론합니다
3. 개발 환경을 설정합니다:
   ```bash
   # 가상환경 생성 및 활성화
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   
   # 의존성 설치
   pip install -r requirements.txt
   
   # Pre-commit hooks 설치
   pre-commit install
   ```
4. 새로운 기능을 개발합니다
5. 코드 품질 검사를 실행합니다:
   ```bash
   # 자동 포맷팅
   black . && isort . --profile=black
   
   # 코드 품질 검사
   flake8 . --max-line-length=88 --extend-ignore=E203
   ```
6. 테스트를 작성하고 실행합니다:
   ```bash
   pytest --cov=. --cov-report=html
   ```
7. Pull Request를 생성합니다

### 코드 스타일
- **Python**: PEP 8 준수 (Black으로 자동 포맷팅)
- **Import**: isort를 사용한 자동 정렬
- **함수/클래스**: docstring 포함 필수
- **변수명**: 명확하고 설명적인 이름 사용
- **라인 길이**: 88자 제한 (Black 기본값)
- **Pre-commit**: 모든 커밋 전 자동 검사 실행

### Docker 개발 환경
```bash
# 개발 환경 시작
./docker-compose-dev.sh up

# 코드 수정 후 자동 리로드 확인
# 로그 확인
./docker-compose-dev.sh logs

# API 테스트
./docker-compose-dev.sh test
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🚀 배포 체크리스트

### Docker 배포
- [ ] Docker 이미지 빌드 성공
- [ ] 컨테이너 실행 및 헬스체크 통과
- [ ] API 엔드포인트 정상 작동
- [ ] 로그 확인 및 모니터링

---

**이 API를 통해 BE/AI에서 차트 디자인과 데이터를 고정하고, FE는 바인딩만 하면 되므로 일관된 차트를 빠르게 구현할 수 있습니다!** 🎉

**Docker를 통해 간단하고 안정적인 배포가 가능합니다!** 🐳
