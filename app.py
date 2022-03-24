from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

# Sets up connection to ElephantSQL Database
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rdbxscrg:ry0nqAde0R4mOupouZfsN2a_ykNNEAYO@kashin.db.elephantsql.com/rdbxscrg'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create a vehicle table


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(200))
    model = db.Column(db.String(200))
    year = db.Column(db.Integer)
    color = db.Column(db.String(200))
    price = db.Column(db.Integer)

# Constructor for table


def __init__(self, make, model, year, color, price):
    self.make = make
    self.model = model
    self.year = year
    self.color = color
    self.price = price

# Returns user to home page


@app.route('/')
def index():
    return render_template('index.html')

# Code for Search button
# TODO: insert code for SQL queries


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        price = request.form['price']
        print(make, model, year, color, price)
        if make == '' or model == '' or year == '' or color == '' or price == '':
            return render_template('index.html', message='Please enter required fields')
        return render_template('success.html')


if __name__ == '__main__':
    #app.debug = True
    app.run()
