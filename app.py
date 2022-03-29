import psycopg2
from psycopg2 import Error
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

hostname = 'kashin.db.elephantsql.com'
database = 'rdbxscrg'
username = 'rdbxscrg'
pwd = 'ry0nqAde0R4mOupouZfsN2a_ykNNEAYO'
port_id = '5432'

# Returns user to home page


@app.route('/')
def index():
    return render_template('index.html')

# Code for Search button


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        price = request.form['price']
        # Prints user selection
        #print(make, model, year, color, price)

        if make == '' or model == '' or year == '' or color == '' or price == '':
            return render_template('index.html', message='Please enter required fields')

    # Connects to elephantSQL database and performs queries based on users selections
    try:
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )

        # SELECT query based on users selections
        sql_select_Query = """select * from car where c_make = %s and c_model = %s and c_year = %s and c_color = %s"""
        cursor = conn.cursor()
        # Executing the query
        cursor.execute(sql_select_Query, [make, model, year, color])
        conn.commit()
        # get all records
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
        # Displays user selected query
        print("\nPrinting each row")
        for row in records:
            print("Cid = ", row[0], )
            print("Sid = ", row[1])
            print("Make  = ", row[2])
            print("Model  = ", row[3])
            print("Year  = ", row[4])
            print("Color  = ", row[5])
            print("Price  = ", row[6])
            print("ZipCode  = ", row[7])
            print("Engine  = ", row[8])
            print("Transmission  = ", row[9], "\n")

        #cursor = conn.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(conn.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

            return render_template('success.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
