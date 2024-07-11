# Homework

Application that will periodically scrape news servers and store headers and URL of its articles.
The application will store the data into its own DB, and it will publish a REST API which will allow for browsing 
articles' metadata by keywords. In case a news server is unavailable, the application should handle it gracefully.

- Included a simple web UI in React for browsing the article's metadata by keywords.
- Implemented basic tests needed for the application components.

For the implementation used offered app skeleton

Requirements:
- Python 3.8+, `pip`
- docker and docker-compose
- Node.js 20.15.0, `npm`
## Setup

- Backend
```bash
# Virtual env creation
python3.8 -m venv .venv

# Dependencies installation
.venv/bin/pip install -U pip
.venv/bin/pip install -U pipenv
.venv/bin/pipenv install

# Run docker container with DB
docker-compose down -t1
docker-compose up -d --build

# Create an empty DB
.venv/bin/python -m app.setup
```
- FE
```bash
# Dependencies installation
.frondend/ npm install

# run tests (optional)
.frondend/ npm run test 
```
## Launching the whole app

Components:
- BE
```bash
.venv/bin/python -m app.scraper
.venv/bin/python -m app.api
```

- FE 
```bash
.frondend/ npm run dev
```
Testing the REST API:

```bash
curl --request POST 'http://localhost:5000/articles/find' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "keywords": [
            "keyword1",
            "anotherkeyword"
        ]
    }'
```
