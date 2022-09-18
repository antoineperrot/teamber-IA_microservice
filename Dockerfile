FROM python:3.8-slim

COPY . /app/src

WORKDIR /app/src

CMD ["ls"]

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn","main:app","--host=0.0.0.0"]