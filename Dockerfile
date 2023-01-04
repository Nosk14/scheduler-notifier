FROM python:3.8-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY scheduler-notifier /usr/local/app/
WORKDIR /usr/local/app/
CMD python3 scheduler.py