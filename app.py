from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:@localhost/data_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qdbozqbbnflzri:17cf00217e6425525281c58a2db42ef73bf6025c281b1885a7860eedfc14e7b3@ec2-54-221-236-144.compute-1.amazonaws.com:5432/d7vf02jucm0m0t?sslmode=require'

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
            avg_height = db.session.query(func.avg(Data.height)).scalar()
            avg_height = round(avg_height)
            count = db.session.query(Data.height).count()
            send_email(email, height, avg_height, count)
            return render_template('success.html')
        return render_template('index.html', text="Email already in system. Please enter a new email address.")


if __name__ == '__main__':
    app.debug = True
    app.run()
