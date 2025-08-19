#!/bin/bash

echo "🚀 가맹점수 분석 차트 API 서버 시작..."
echo ""

# 가상환경 활성화 (있는 경우)
if [ -d ".venv" ]; then
    echo "📦 가상환경 활성화 중..."
    source .venv/bin/activate
fi

# 의존성 설치 확인
echo "🔍 의존성 확인 중..."
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Flask 설치 중..."
    pip install -r requirements.txt
fi

# 서버 실행
echo "🌐 서버 시작 중..."
echo "📍 서버 주소: http://localhost:5000"
echo "📊 API 문서: http://localhost:5000/"
echo "💚 헬스 체크: http://localhost:5000/health"
echo ""
echo "🛑 서버 중지: Ctrl+C"
echo ""

python app.py
