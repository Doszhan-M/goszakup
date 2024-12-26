docker logs -f goszakup-dashboard-1
docker logs -f goszakup-beat_dashboard-1
docker exec -it goszakup-dashboard-1 bash

python manage.py createsuperuser  
admin:aCiOnIQuArdE  
python manage.py makemigrations  
python manage.py migrate  

find . -name __pycache__ -exec rm -rf {} \;

python3 -m grpc_tools.protoc \
    -I./signer/protos \
    --python_out=./signer/pb2 \
    --pyi_out=./signer/pb2 \
    --grpc_python_out=./signer/pb2 \
    eds.proto

sudo kill -9 $(sudo lsof -t -i :8000)
