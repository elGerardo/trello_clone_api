FROM python:3.11

WORKDIR /home/node/app

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "trelloApi.wsgi"]
