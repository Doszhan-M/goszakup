FROM python:3.12.2-bookworm


ENV TZ=Asia/Almaty \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:0


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

WORKDIR /tender/

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

COPY app/ ./app/

ENTRYPOINT ["bash", "/tender/app/sh/start.sh"]

# docker не настраивается, потому что в контейнере требуется NCALayer
