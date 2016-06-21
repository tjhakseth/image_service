from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

class Profile(db.Model):
    """profiles"""

    __tablename__ = "profiles"

    username = db.Column(db.String(50), primary_key=True)
    api_token = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    full_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):

        return "<Profile username=%s, api_token=%s>" % (self.username, self.api_token)



def connect_to_db(app, connection_string):
    """Connect the database to our Flask app."""
    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."