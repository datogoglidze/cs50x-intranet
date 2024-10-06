FROM python:3.11.7

WORKDIR /code

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY intranet ./intranet

CMD ["python", "-m", "intranet.runner", "--host", "0.0.0.0", "--port", "8001"]
