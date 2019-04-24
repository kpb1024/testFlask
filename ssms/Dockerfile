FROM python:2

COPY . /app/

RUN pip install -r /app/requirements.txt

RUN export FLASK_APP=ssms
RUN export FLASK_ENV=development

EXPOSE 5002

ENTRYPOINT ["python", "main.py"]
