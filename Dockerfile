FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

# Dodaj model NLP po instalacji spaCy
RUN python3 -m spacy download en_core_web_sm

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
