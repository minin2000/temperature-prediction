FROM joyzoursky/python-chromedriver:3.9

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV AM_I_IN_A_DOCKER_CONTAINER Yes
