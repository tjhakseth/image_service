"""Image Service Project"""
from flask import Flask, request, jsonify
from model import connect_to_db, db, Profile

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    """Landing page for project"""
    return "Hello World"


@app.route('/profiles', methods=['GET'])
def new_user_form():
    """Creates and stores new user"""
    return jsonify(success=True)


@app.route('/profiles', methods=['POST'])
def process_new_user():
    """Creates and stores new user"""

    username = request.form["username"]
    date_of_birth = request.form["date_of_birth"]
    full_name = request.form["full_name"]

    new_profile = Profile(
        username=username,
        api_token="bananas",
        date_of_birth=date_of_birth,
        full_name=full_name
    )

    db.session.add(new_profile)
    db.session.commit()

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
    connect_to_db(app)
