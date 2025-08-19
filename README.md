# 🚀 가맹점수 분석 차트 API 서버

**FE에서 차트 사양을 가져올 수 있는 REST API를 제공합니다.**

> 🎯 **목적**: 프론트엔드 개발자가 차트 라이브러리별 사양(spec)을 쉽게 가져와서 차트를 렌더링할 수 있도록 지원

## 📋 목차

- [✨ 주요 기능](#-주요-기능)
- [📊 제공하는 차트](#-제공하는-차트)
- [🛠️ 지원하는 차트 라이브러리](#️-지원하는-차트-라이브러리)
- [🚀 빠른 시작](#-빠른-시작)
- [📡 API 엔드포인트](#-api-엔드포인트)
- [📚 API 문서](#-api-문서)
- [🔧 사용 예시](#-사용-예시)
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

### 테스트 데이터
`data` 폴더 내 CSV 파일들이 자동으로 포함되어 있습니다:
- `지역별_도소매별_가맹점수_현황.csv`
- `지역별_서비스별_가맹점수_현황.csv`
- `지역별_외식별_가맹점수_현황.csv`

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

## 🛠️ 개발 및 배포

### 개발 모드
```bash
# 개발 서버 실행 (자동 재시작, 디버그 모드)
python app.py

# 또는 환경변수 설정
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### 프로덕션 배포
```bash
# Gunicorn 사용 (권장)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app

# 또는 uWSGI 사용
pip install uwsgi
uwsgi --http :5001 --wsgi-file app.py --callable app
```

### Docker 배포
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
```

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

### 로그 확인
```bash
# Flask 디버그 로그 활성화
export FLASK_DEBUG=1
python app.py

# 또는 로그 파일로 출력
python app.py > app.log 2>&1
```

## 🤝 기여하기

### 개발 환경 설정
1. 이 저장소를 포크합니다
2. 로컬에 클론합니다
3. 가상환경을 설정하고 의존성을 설치합니다
4. 새로운 기능을 개발합니다
5. 테스트를 작성하고 실행합니다
6. Pull Request를 생성합니다

### 코드 스타일
- Python: PEP 8 준수
- 함수/클래스: docstring 포함
- 변수명: 명확하고 설명적인 이름 사용

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

### 특정 차트 타입만 가져오기
```bash
curl "http://localhost:5000/api/charts/echarts?type=line"
curl "http://localhost:5000/api/charts/echarts?type=bar"
```

## 💻 FE에서 사용하기

### JavaScript/TypeScript 예시

```javascript
// ECharts 라인 차트 사양 가져오기
async function getEChartsLineChart() {
    try {
        const response = await fetch('http://localhost:5000/api/charts/echarts/line');
        const chartOption = await response.json();
        
        // ECharts로 차트 렌더링
        const chart = echarts.init(document.getElementById('chart'));
        chart.setOption(chartOption);
    } catch (error) {
        console.error('차트 사양 가져오기 실패:', error);
    }
}

// 모든 차트 사양 가져오기
async function getAllCharts() {
    try {
        const response = await fetch('http://localhost:5000/api/charts');
        const allCharts = await response.json();
        
        console.log('사용 가능한 차트:', allCharts);
        
        // 원하는 차트 라이브러리 선택
        const echartsOption = allCharts.echarts.line_chart;
        const plotlyOption = allCharts.plotly.bar_chart;
        
    } catch (error) {
        console.error('차트 사양 가져오기 실패:', error);
    }
}
```

### Python 예시

```python
import requests

# ECharts 라인 차트 사양 가져오기
response = requests.get('http://localhost:5000/api/charts/echarts/line')
if response.status_code == 200:
    chart_option = response.json()
    print("차트 사양:", chart_option)
else:
    print("API 호출 실패:", response.status_code)
```

## 📁 파일 구조

```
08_chart_api_server/
├── app.py                    # Flask API 서버 (Swagger/ReDoc 포함)
├── chart_specs.py           # 차트 사양 정의 (CSV 데이터 로드)
├── test_chart_specs.py      # 차트 사양 테스트
├── test_api_client.py       # API 테스트 클라이언트
├── requirements.txt          # Python 의존성
├── data/                    # CSV 데이터 파일
│   ├── 지역별_도소매별_가맹점수_현황.csv
│   ├── 지역별_서비스별_가맹점수_현황.csv
│   └── 지역별_외식별_가맹점수_현황.csv
└── README.md                # 이 파일
```

## 📊 데이터 소스

- **데이터 형식**: CSV 파일
- **데이터 위치**: `data/` 폴더
- **데이터 내용**: 2017년~2024년 업종별 가맹점수 현황
- **동적 로드**: CSV 파일에서 실시간으로 데이터 로드

## 🔍 API 응답 예시

### ECharts 라인 차트 응답
```json
{
  "title": {
    "text": "연도별 업종별 총 가맹점수 추이",
    "left": "center",
    "textStyle": {"fontSize": 16, "fontWeight": "bold"}
  },
  "xAxis": {
    "type": "category",
    "data": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "name": "연도"
  },
  "yAxis": {
    "type": "value",
    "name": "총 가맹점수"
  },
  "series": [
    {
      "name": "도소매",
      "type": "line",
      "data": [48324, 54194, 55581, 56897, 60874, 63470, 59843, 69293]
    }
  ]
}
```

## 🎯 장점

1. **일관성**: BE/AI에서 차트 디자인과 데이터를 고정
2. **유연성**: FE에서 원하는 차트 라이브러리 선택 가능
3. **재사용성**: 동일한 데이터로 여러 차트 라이브러리 지원
4. **유지보수성**: 차트 사양 변경 시 API만 수정하면 됨

## 🚨 주의사항

1. **CORS**: 개발 환경에서만 모든 도메인 허용 (프로덕션에서는 제한 필요)
2. **에러 처리**: FE에서 API 호출 실패 시 적절한 에러 처리 필요
3. **캐싱**: 자주 변경되지 않는 차트 사양은 FE에서 캐싱 고려

## 🤝 협업 가이드

### BE/AI 개발자
- 차트 사양 생성 및 유지보수
- API 서버 운영
- 데이터 업데이트

### FE 개발자
- API 호출 및 차트 렌더링
- 사용자 인터랙션 추가
- 차트 라이브러리 선택

## 📞 지원

API 사용 중 문제가 발생하면 다음을 확인하세요:

1. 서버가 실행 중인지 확인 (`/health` 엔드포인트)
2. API 엔드포인트 URL이 올바른지 확인
3. 요청/응답 형식이 올바른지 확인

---

**이 API를 통해 BE/AI에서 차트 디자인과 데이터를 고정하고, FE는 바인딩만 하면 되므로 일관된 차트를 빠르게 구현할 수 있습니다!** 🎉
