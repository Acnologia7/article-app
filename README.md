# Homework

Application that will periodically scrape news servers and store headers and URL of its articles.
The application will store the data into its own DB, and it will publish a REST API which will allow for browsing 
articles' metadata by keywords. In case a news server is unavailable, the application should handle it gracefully.

- Included a simple web UI in React for browsing the article's metadata by keywords.
- Implemented basic tests needed for the application components.

For the implementation used offered app skeleton

Extra note:
- Conteinerization not done due time (wanted to finish till the end of this week), if you are interested how I did conternerization, check my other project here:
same goes for using .env variables and customization of services etc.
https://github.com/Acnologia7/img-sorter-by-color

- added some commentary into code to clarify why I modified some things from skeleton (db model check for unique on URL etc.)
- but mostly I wanted to preserve it as much as possible
- scrapers are scrapping articles from homepages of news servers only, would be better to have some kind of automated browsing (via selenium and headless broser) due to websites being dynamic, but for demonstration I hope it is ok.
- some variables are hardcoded which is not ok, but as stated above, wanted to put it out fast as prototype
- scheduler is simple while loop, I think it is little bit of overkill, but my choice would be otherwise Celery or APScheduler for scrapers (or how is most of the time done by a chron job)
- UI is just simple the most basic Page just to demonstrate connection between FE and BE using API and showing results.


Requirements:
- Python 3.12, `pip`
- docker and docker-compose
- Node.js 20.15.0, `npm`
## Setup

- Backend
```bash
# Virtual env creation
python3.12 -m venv .venv

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
