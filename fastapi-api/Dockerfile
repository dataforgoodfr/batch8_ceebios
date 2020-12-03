FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /src/
COPY ./src /src

# ENV PYTHONPATH=$PWD

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

