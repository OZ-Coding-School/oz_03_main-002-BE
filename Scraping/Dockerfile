# python 베이스 이미지 사용
FROM python:3.9-slim-buster

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-noto-cjk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# python 패키지 설치
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# 스크립트 파일 복사
COPY test.py .

# 실행 명령어 설정 (xvfb 추가)
CMD ["xvfb-run", "-a", "python3", "test.py"]
