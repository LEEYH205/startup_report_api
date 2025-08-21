#!/bin/bash

# 가맹점수 분석 차트 API 서버 Docker 빌드 및 실행 스크립트

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
    echo "  build       도커 이미지 빌드"
    echo "  run         도커 컨테이너 실행"
    echo "  stop        도커 컨테이너 중지"
    echo "  restart     도커 컨테이너 재시작"
    echo "  logs        도커 컨테이너 로그 확인"
    echo "  clean       도커 이미지 및 컨테이너 정리"
    echo "  dev         개발 모드로 실행 (핫 리로드)"
    echo "  test        도커 컨테이너 테스트"
    echo "  help        이 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0 build    # 이미지 빌드"
    echo "  $0 run      # 컨테이너 실행"
    echo "  $0 dev      # 개발 모드 실행"
}

# 도커 이미지 빌드
build_image() {
    log_info "도커 이미지 빌드 중..."
    
    # 기존 이미지가 있는지 확인
    if docker image inspect chart-api-server:latest >/dev/null 2>&1; then
        log_warning "기존 이미지가 있습니다. 제거하시겠습니까? (y/N)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            docker rmi chart-api-server:latest
        fi
    fi
    
    docker build -t chart-api-server:latest .
    log_success "도커 이미지 빌드 완료: chart-api-server:latest"
}

# 도커 컨테이너 실행
run_container() {
    log_info "도커 컨테이너 실행 중..."
    
    # 기존 컨테이너가 실행 중인지 확인
    if docker ps -q -f name=chart-api-server | grep -q .; then
        log_warning "컨테이너가 이미 실행 중입니다."
        return 1
    fi
    
    # 기존 컨테이너가 있는지 확인하고 제거
    if docker ps -aq -f name=chart-api-server | grep -q .; then
        log_info "기존 컨테이너 제거 중..."
        docker rm chart-api-server
    fi
    
    docker run -d \
        --name chart-api-server \
        -p 5001:5001 \
        -v "$(pwd)/data:/app/data:ro" \
        -v "$(pwd)/chart_specs_json:/app/chart_specs_json:ro" \
        --restart unless-stopped \
        chart-api-server:latest
    
    log_success "도커 컨테이너 실행 완료"
    log_info "API 서버가 http://localhost:5001 에서 실행 중입니다."
}

# 개발 모드 실행
run_dev() {
    log_info "개발 모드로 도커 컨테이너 실행 중..."
    
    # 기존 컨테이너가 실행 중인지 확인
    if docker ps -q -f name=chart-api-server-dev | grep -q .; then
        log_warning "개발 컨테이너가 이미 실행 중입니다."
        return 1
    fi
    
    # 기존 컨테이너가 있는지 확인하고 제거
    if docker ps -aq -f name=chart-api-server-dev | grep -q .; then
        log_info "기존 개발 컨테이너 제거 중..."
        docker rm chart-api-server-dev
    fi
    
    # 개발용 이미지 빌드
    if ! docker image inspect chart-api-server:dev >/dev/null 2>&1; then
        log_info "개발용 도커 이미지 빌드 중..."
        docker build -t chart-api-server:dev -f Dockerfile.dev .
    fi
    
    docker run -d \
        --name chart-api-server-dev \
        -p 5002:5001 \
        -v "$(pwd):/app" \
        -v "$(pwd)/data:/app/data:ro" \
        -v "$(pwd)/chart_specs_json:/app/chart_specs_json:ro" \
        --restart unless-stopped \
        chart-api-server:dev
    
    log_success "개발 모드 도커 컨테이너 실행 완료"
    log_info "API 서버가 http://localhost:5002 에서 실행 중입니다. (핫 리로드 활성화)"
}

# 도커 컨테이너 중지
stop_container() {
    log_info "도커 컨테이너 중지 중..."
    
    if docker ps -q -f name=chart-api-server | grep -q .; then
        docker stop chart-api-server
        log_success "프로덕션 컨테이너 중지 완료"
    fi
    
    if docker ps -q -f name=chart-api-server-dev | grep -q .; then
        docker stop chart-api-server-dev
        log_success "개발 컨테이너 중지 완료"
    fi
}

# 도커 컨테이너 재시작
restart_container() {
    log_info "도커 컨테이너 재시작 중..."
    stop_container
    sleep 2
    run_container
}

# 도커 컨테이너 로그 확인
show_logs() {
    if docker ps -q -f name=chart-api-server | grep -q .; then
        log_info "프로덕션 컨테이너 로그:"
        docker logs -f chart-api-server
    elif docker ps -q -f name=chart-api-server-dev | grep -q .; then
        log_info "개발 컨테이너 로그:"
        docker logs -f chart-api-server-dev
    else
        log_warning "실행 중인 컨테이너가 없습니다."
    fi
}

# 도커 컨테이너 테스트
test_container() {
    log_info "도커 컨테이너 테스트 중..."
    
    # 컨테이너가 실행 중인지 확인
    if ! docker ps -q -f name=chart-api-server | grep -q . && ! docker ps -q -f name=chart-api-server-dev | grep -q .; then
        log_error "실행 중인 컨테이너가 없습니다. 먼저 컨테이너를 실행하세요."
        return 1
    fi
    
    # 포트 확인
    local port=5001
    if docker ps -q -f name=chart-api-server-dev | grep -q .; then
        port=5002
    fi
    
    # API 헬스체크
    log_info "API 헬스체크 테스트..."
    if curl -f "http://localhost:$port/health" >/dev/null 2>&1; then
        log_success "API 서버가 정상적으로 응답하고 있습니다."
    else
        log_error "API 서버 응답 실패"
        return 1
    fi
    
    # API 엔드포인트 테스트
    log_info "API 엔드포인트 테스트..."
    if curl -f "http://localhost:$port/api/charts" >/dev/null 2>&1; then
        log_success "차트 API 엔드포인트 정상 작동"
    else
        log_error "차트 API 엔드포인트 테스트 실패"
        return 1
    fi
    
    log_success "모든 테스트 통과!"
}

# 도커 이미지 및 컨테이너 정리
clean_docker() {
    log_info "도커 이미지 및 컨테이너 정리 중..."
    
    # 실행 중인 컨테이너 중지
    stop_container
    
    # 컨테이너 제거
    if docker ps -aq -f name=chart-api-server | grep -q .; then
        docker rm chart-api-server
    fi
    
    if docker ps -aq -f name=chart-api-server-dev | grep -q .; then
        docker rm chart-api-server-dev
    fi
    
    # 이미지 제거
    if docker image inspect chart-api-server:latest >/dev/null 2>&1; then
        docker rmi chart-api-server:latest
    fi
    
    if docker image inspect chart-api-server:dev >/dev/null 2>&1; then
        docker rmi chart-api-server:dev
    fi
    
    # 사용하지 않는 이미지 정리
    docker image prune -f
    
    log_success "도커 정리 완료"
}

# 메인 로직
case "${1:-help}" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    dev)
        run_dev
        ;;
    stop)
        stop_container
        ;;
    restart)
        restart_container
        ;;
    logs)
        show_logs
        ;;
    test)
        test_container
        ;;
    clean)
        clean_docker
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
