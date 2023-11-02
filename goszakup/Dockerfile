FROM python:3.11.6-slim-bullseye


EXPOSE 8000

ENV TZ=Asia/Almaty \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# Install Google Chrome and Chromedriver 
RUN apt update && apt install wget curl jq unzip -y && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install ./google-chrome-stable_current_amd64.deb -y && apt clean && \
    wget https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json -O json_data.json && \
    CHROMEDRIVER_URL=$(jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform == "linux64") | .url' json_data.json) && \
    wget "$CHROMEDRIVER_URL" -O chromedriver.zip && \
    unzip -j ./chromedriver.zip 'chromedriver-linux64/chromedriver' -d  /usr/local/bin/ && \
    rm ./google-chrome-stable_current_amd64.deb && \
    rm ./chromedriver.zip && \
    rm ./json_data.json
    
WORKDIR /egov/

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN useradd -ms /bin/bash appuser && \ 
    chown -R appuser:appuser ./
USER appuser

ENTRYPOINT [ "./app/sh/run_app.sh" ]
