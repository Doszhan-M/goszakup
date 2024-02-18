FROM python:3.12.2-bookworm


EXPOSE 8000

ENV TZ=Asia/Almaty \
    # PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99

# Install Google Chrome and Chromedriver 
RUN apt update && apt install wget curl jq unzip -y && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install ./google-chrome-stable_current_amd64.deb -y && \
    wget https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json -O json_data.json && \
    CHROMEDRIVER_URL=$(jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform == "linux64") | .url' json_data.json) && \
    wget "$CHROMEDRIVER_URL" -O chromedriver.zip && \
    unzip -j ./chromedriver.zip 'chromedriver-linux64/chromedriver' -d  /usr/local/bin/ && \
    rm ./google-chrome-stable_current_amd64.deb && \
    rm ./chromedriver.zip && \
    rm ./json_data.json

# Install PyAutoGUI dependencies
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-xlib python3-tk python3-dev xvfb xserver-xephyr python3-tk python3-dev gnome-screenshot && apt clean 
RUN Xvfb :99 -ac &

WORKDIR /goszakup/

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/





RUN export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
RUN apt-get update && apt-get install -y openjdk-17-jre iproute2 vim-common bsdmainutils libnotify-bin dbus-x11 dunst
COPY ncalayer/ /ncalayer/

# RUN useradd /bin/bash appuser && \ 
#     chown -R appuser:appuser ./
# RUN yes | /ncalayer/ncalayer/ncalayer.sh --nogui

# /ncalayer/ncalayer/ncalayer.sh --run

# RUN useradd -ms /bin/bash appuser && \ 
#     chown -R appuser:appuser ./
# USER appuser

ENTRYPOINT [ "./app/sh/run_app.sh" ]
