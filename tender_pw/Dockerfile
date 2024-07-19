FROM python:3.12.2-bookworm


ENV TZ=Asia/Almaty \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99


WORKDIR /goszakup/

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/


ENTRYPOINT [ "uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload" ]
