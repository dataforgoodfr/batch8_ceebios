FROM python:3.7

# update the package repository and install Tor
RUN apt update
RUN apt install -y tor

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY data/scimagojr/scimagojr2019.csv scimagojr2019.csv
COPY build.sh ./
COPY setup.sh ./
COPY index.py ./
COPY pokedex ./pokedex
COPY app ./app

CMD sh setup.sh && streamlit run index.py