FROM python:3.10.12

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5432

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

CMD ["python", "main.py"]