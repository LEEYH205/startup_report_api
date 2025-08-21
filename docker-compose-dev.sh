#!/bin/bash

# Docker Compose 개발 환경 관리 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 도움말 함수
show_help() {
    echo "사용법: $0 [옵션]"
    echo ""
    echo "옵션:"
    echo "  up          개발 환경 시작 (핫 리로드)"
    echo "  down        개발 환경 중지"
    echo "  restart     개발 환경 재시작"
    echo "  logs        로그 확인"
    echo "  build       이미지 재빌드"
    echo "  status      상태 확인"
    echo "  test        API 테스트"
    echo "  help        이 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0 up       # 개발 환경 시작"
    echo "  $0 down     # 개발 환경 중지"
    echo "  $0 logs     # 로그 확인"
}

# 개발 환경 시작
start_dev() {
    log_info "개발 환경 시작 중..."
    
    # 기존 컨테이너가 실행 중인지 확인
    if docker-compose ps | grep -q "Up"; then
        log_warning "개발 환경이 이미 실행 중입니다."
        return 1
    fi
    
    # 개발 프로필로 시작
    docker-compose --profile dev up -d
    
    log_success "개발 환경 시작 완료"
    log_info "API 서버가 http://localhost:5002 에서 실행 중입니다. (핫 리로드 활성화)"
    log_info "Swagger UI: http://localhost:5002/docs"
    log_info "ReDoc: http://localhost:5002/redoc"
}

# 개발 환경 중지
stop_dev() {
    log_info "개발 환경 중지 중..."
    docker-compose down
    log_success "개발 환경 중지 완료"
}

# 개발 환경 재시작
restart_dev() {
    log_info "개발 환경 재시작 중..."
    stop_dev
    sleep 2
    start_dev
}

# 로그 확인
show_logs() {
    log_info "개발 환경 로그 확인 중..."
    docker-compose logs -f chart-api-dev
}

# 이미지 재빌드
rebuild_dev() {
    log_info "개발용 이미지 재빌드 중..."
    docker-compose build --no-cache chart-api-dev
    log_success "이미지 재빌드 완료"
}

# 상태 확인
show_status() {
    log_info "개발 환경 상태 확인 중..."
    docker-compose ps
}

# API 테스트
test_api() {
    log_info "API 테스트 중..."
    
    # 컨테이너가 실행 중인지 확인
    if ! docker-compose ps | grep -q "Up"; then
        log_error "개발 환경이 실행 중이지 않습니다. 먼저 'up' 명령어로 시작하세요."
        return 1
    fi
    
    # API 헬스체크
    log_info "API 헬스체크 테스트..."
    if curl -f "http://localhost:5002/health" >/dev/null 2>&1; then
        log_success "API 서버가 정상적으로 응답하고 있습니다."
    else
        log_error "API 서버 응답 실패"
        return 1
    fi
    
    # API 엔드포인트 테스트
    log_info "API 엔드포인트 테스트..."
    if curl -f "http://localhost:5002/api/charts" >/dev/null 2>&1; then
        log_success "차트 API 엔드포인트 정상 작동"
    else
        log_error "차트 API 엔드포인트 테스트 실패"
        return 1
    fi
    
    # Swagger UI 테스트
    log_info "Swagger UI 테스트..."
    if curl -f "http://localhost:5002/docs" >/dev/null 2>&1; then
        log_success "Swagger UI 정상 작동"
    else
        log_error "Swagger UI 테스트 실패"
        return 1
    fi
    
    log_success "모든 테스트 통과!"
}

# 메인 로직
case "${1:-help}" in
    up)
        start_dev
        ;;
    down)
        stop_dev
        ;;
    restart)
        restart_dev
        ;;
    logs)
        show_logs
        ;;
    build)
        rebuild_dev
        ;;
    status)
        show_status
        ;;
    test)
        test_api
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "알 수 없는 옵션: $1"
        show_help
        exit 1
        ;;
esac
