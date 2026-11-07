FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 -r requirements.txt

COPY . .

RUN pip install -e .


CMD [ "python", "main.py" ]
