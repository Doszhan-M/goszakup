FROM ubuntu:bionic

RUN apt-get update && apt-get install python3 tesseract-ocr python3-pip curl unzip -yf
# Install Chrome
RUN apt-get update -y
RUN apt-get install -y dbus-x11
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb
RUN apt-get -y install libssl1.0-dev
RUN curl https://chromedriver.storage.googleapis.com/87.0.4280.20/chromedriver_linux64.zip -o /usr/local/bin/chromedriver.zip
RUN cd /usr/local/bin && unzip chromedriver.zip
RUN chmod +x /usr/local/bin/chromedriver
USER root
RUN apt update
RUN apt-get install -y poppler-utils
RUN apt-get clean
RUN apt install -y python3 python3-pip
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-xlib python3-tk python3-dev
RUN apt install -y xvfb xserver-xephyr python3-tk python3-dev
RUN Xvfb :99 -ac &
RUN export DISPLAY=:99
RUN pip3 install virtualenv
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN virtualenv .venv
RUN /bin/bash -c "source .venv/bin/activate"
RUN pip3 install -r requirements.txt
RUN apt-get install -y scrot
COPY . /app
ENTRYPOINT [ "python3", "scrapper.py" ]