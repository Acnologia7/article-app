from http import HTTPStatus
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import DBAPIError

try:
    from app import db
    from app.service import get_articles_with_keywords
except ImportError:
    import db
    from service import get_articles_with_keywords


app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.teardown_request
def remove_db_session(exception=None):
    """Remove the database session at the end of the request."""
    db.session.remove()


@app.route("/articles/find", methods=["POST"])
def find_articles():
    """
    Handle POST request to find articles with given keywords.
    Returns:
        HTTP 422 if the query in request.json is not valid.
        JSON response with articles matching the given keywords.
    """
    data = request.json

    if not data or not isinstance(data.get("keywords"), list):
        abort(HTTPStatus.UNPROCESSABLE_ENTITY)

    keywords = data["keywords"]

    try:
        articles = get_articles_with_keywords(keywords)
        articles_list = [
            {"header": article.header, "url": article.url} for article in articles
        ]

        return jsonify({"articles": articles_list}), HTTPStatus.OK

    except DBAPIError:
        abort(HTTPStatus.SERVICE_UNAVAILABLE)
    except Exception:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    app.run(debug=True)
