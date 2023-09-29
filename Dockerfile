from python:3.10-slim-buster

RUN apt update -y && apt install -awscli -y
WORKDIR /app

copy . /app

RUN pip install -r requirements.txt
RUN pip install --upgrade accelerate
RUN pip uninstall -y transformers accelerate
RUN pip install transformers accelerate

CMD ["python3", "app.py"]