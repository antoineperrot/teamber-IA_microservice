FROM python:3.8-slim

COPY ./src /app/src

WORKDIR /app/src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn","main:app","--host=0.0.0.0"]