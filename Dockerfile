FROM python:3

WORKDIR /app

COPY lockrelay/ ./
RUN pip3 install -r requirements.txt


CMD [ "python3", "-u" , "web.py"]
