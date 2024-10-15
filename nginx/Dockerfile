
FROM nginx:latest

WORKDIR /etc/nginx

COPY nginx.conf /etc/nginx/nginx.conf

# Копируем сертификаты
COPY certs /etc/nginx/certs

CMD ["nginx", "-g", "daemon off;"]
