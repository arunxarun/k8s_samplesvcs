FROM python:2.7.13


COPY ./src /src


WORKDIR /src
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "server.py"]

EXPOSE 8080
