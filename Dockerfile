# 멀티스테이지 빌드를 위한 베이스 이미지
FROM python:3.11-slim as builder

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로덕션 이미지
FROM python:3.11-slim

# 메타데이터 설정
LABEL maintainer="LEEYH205"
LABEL description="창업 리포트 차트 API 서버"
LABEL version="1.0.0"

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 사용자 생성 (보안 강화)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Python 의존성 복사 (시스템 레벨에 설치됨)
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 애플리케이션 코드 복사
COPY . .

# 데이터 폴더 권한 설정
RUN chown -R appuser:appuser /app

# 포트 노출
EXPOSE 5001

# 환경변수 설정
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5001

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# 사용자 변경
USER appuser

# 애플리케이션 실행
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]
