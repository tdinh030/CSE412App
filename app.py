import webbrowser
import psycopg2
import os
import re
from bs4 import BeautifulSoup as bs
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
        p = []
        tbl = "<tr><td>Make</td><td>Model</td><td>Year</td><td>Color</td><td>Price</td><td>ZipCode</td><td>Engine</td><td>Transmission</td></tr>"
        p.append(tbl)
        # Displays user selected query
        print("\nPrinting each row")
        for row in records:
            print("Cid = ", row[0], )
            print("Sid = ", row[1])
            print("Make  = ", row[2])
            a = "<tr><td>%s</td>" % row[2]
            p.append(a)
            print("Model  = ", row[3])
            b = "<td>%s</td>" % row[3]
            p.append(b)
            print("Year  = ", row[4])
            c = "<td>%s</td>" % row[4]
            p.append(c)
            print("Color  = ", row[5])
            d = "<td>%s</td>" % row[5]
            p.append(d)
            print("Price  = ", row[6])
            e = "<td>%s</td>" % row[6]
            p.append(e)
            print("ZipCode  = ", row[7])
            f = "<td>%s</td>" % row[7]
            p.append(f)
            print("Engine  = ", row[8])
            g = "<td>%s</td>" % row[8]
            p.append(g)
            print("Transmission  = ", row[9], "\n")
            h = "<td>%s</td></tr>" % row[9]
            p.append(h)

        contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
        <meta content="text/html; charset=ISO-8859-1"
        http-equiv="content-type">
        <title>Python Webbrowser</title>
        </head>
        <body>
        <table>
        %s
        </table>
        </body>
        </html>
        ''' % (p)

        filename = 'webbrowser.html'
        output = open(filename, "w")
        output.write(contents)
        output.close()
        webbrowser.open(filename)

#        base = os.path.dirname(os.path.abspath(__file__))

#        html = open(os.path.join(base, 'templates/car_listing.html'))

#        soup = bs(html, 'html.parser')

#        old_text = soup.find("dd", {"id": "c_make"})

#        new_text = old_text.find(text=re.compile(
#            'Default')).replace_with(row[2])

#        with open("templates/car_listing.html", "wb") as f_output:
#            f_output.write(soup.prettify("utf-8"))

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
