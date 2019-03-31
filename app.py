from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:@localhost/data_collector'

db = SQLAlchemy(app)


class Data(db.Model):
    """Data Model."""

    __tablename__ = 'height'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        """Init."""
        self.email = email
        self.height = height


@app.route('/')
def index():
    """Home route."""
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    """Success route."""
    if request.method=='POST':
        email = request.form['email_name']
        height = request.form['height']
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()

            return render_template('success.html')
        return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
