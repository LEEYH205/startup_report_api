#!/bin/bash

echo "🚀 가맹점수 분석 차트 API 서버 설정 및 테스트 시작..."
echo ""

# 가상환경이 이미 존재하는지 확인
if [ ! -d ".venv" ]; then
    echo "📦 가상환경 생성 중..."
    python -m venv .venv
    echo "✅ 가상환경 생성 완료"
else
    echo "📦 기존 가상환경 발견"
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source .venv/bin/activate
echo "✅ 가상환경 활성화 완료"

# pip 업그레이드
echo "📥 pip 업그레이드 중..."
pip install --upgrade pip
echo "✅ pip 업그레이드 완료"

# 의존성 설치
echo "📦 의존성 설치 중..."
pip install -r requirements.txt
echo "✅ 의존성 설치 완료"

# 차트 사양 테스트
echo ""
echo "🧪 차트 사양 테스트 실행 중..."
python test_chart_specs.py

echo ""
echo "🎯 설정 및 테스트 완료!"
echo ""
echo "📋 다음 단계:"
echo "1. 서버 실행: ./run_server.sh"
echo "2. API 테스트: python test_api_client.py"
echo "3. 브라우저에서 http://localhost:5001 접속"
