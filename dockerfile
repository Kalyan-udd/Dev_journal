FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e .

CMD [ "python", "main.py" ]
