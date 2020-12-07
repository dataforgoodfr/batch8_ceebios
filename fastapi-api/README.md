## Configure

Set your MongoDB connection string  in `.env`. For example:

_.env_

```
DATABASE_URI = "mongodb://localhost:27017"
DATABASE_NAME = <database/>
```
## Run localy
```
cd src/
python3 -m venv venv
source venv/bin/activate

uvicorn main.app:app --reload
```

## Deploy via Docker Compose
Set up your _.env_ file for production
*db : name of the mongo container 

```
DATABASE_URI = "mongodb://db:27017"
DATABASE_NAME = <database/>
```

Then, you can quickly start via:

```
docker-compose up -d --build
```

Go to http://localhost/docs in your browser!