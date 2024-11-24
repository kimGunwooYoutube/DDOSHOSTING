# 베이스 이미지로 Python 3.9-slim 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 파일 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# Server.py 파일 복사
COPY Server.py .

# 컨테이너 시작 시 실행할 명령어 설정
CMD ["python", "Server.py"]
