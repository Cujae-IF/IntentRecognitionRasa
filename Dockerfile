FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update \
    && apt install -y --no-install-recommends python3-pip python3-venv \
    build-essential python3-dev nano

COPY requirements.txt .

RUN pip3 install --upgrade pip setuptools --user --no-cache-dir
RUN pip3 install wheel --user --no-cache-dir
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN rasa train -c nlu/config.yml -d nlu/domain.yml --out nlu/models/ --data nlu/data/

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]