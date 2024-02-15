FROM python:3.12.2-slim-bullseye


EXPOSE 8000

ENV TZ=Asia/Almaty \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# Install Google Chrome and Chromedriver 
RUN apt update && apt install curl -y
    
WORKDIR /goszakup/

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN useradd -ms /bin/bash appuser && \ 
    chown -R appuser:appuser ./
USER appuser

ENTRYPOINT [ "./app/sh/run_app.sh" ]
