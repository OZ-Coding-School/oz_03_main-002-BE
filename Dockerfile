FROM python:3.12

WORKDIR ./naengttogi

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
# RUN python manage.py migrate

CMD ["python", "manage.py", "runserver"]
