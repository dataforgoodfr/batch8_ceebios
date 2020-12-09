## Configure

Set your MongoDB connection string  in `.env`. For example:

_.env_

```
DATABASE_URI = "mongodb://localhost:27017"
DATABASE_NAME = <database>
```
## Run localy
```
cd src/
python3 -m venv venv
source venv/bin/activate

uvicorn app.main:app --reload
```

## Deploy via Docker Compose
Set up your _.env_ file for production
(*db : name of the mongo container)

```
DATABASE_URI = "mongodb://<username>:<password>@db:27017/admin"
DATABASE_NAME = <database>
MONGO_INITDB_DATABASE=<database>
MONGO_INITDB_ROOT_USERNAME=<username>
MONGO_INITDB_ROOT_PASSWORD=<password>
```

Then, you can quickly start via:
```
docker-compose up -d --build
```

Go to http://localhost/docs in your browser!