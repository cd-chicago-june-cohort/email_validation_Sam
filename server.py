from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'emailval')
app.secret_key = 'validate'

@app.route('/')
def index():
    emails = mysql.query_db('SELECT * FROM emails')
    if 'valid' not in session:
        session['valid'] = 'init'
    #session_hold = session['valid']
    return render_template('index.html', in_db = session['valid'])

@app.route('/success')
def display_success_page():
    emails = mysql.query_db('SELECT * FROM emails')
    return render_template('success.html', email_list = emails)

@app.route('/input', methods=['POST'])
def add_email():
    count = 0
    email_data = {}
    input_address = request.form['address']
    email_data['address'] = input_address
    count_query = "SELECT COUNT(id) FROM emails WHERE address = '" + email_data['address'] +"'"
    count = mysql.query_db(count_query)
    check = count[0].values()
    if check [0] == 0:
        print "Email valid. Not already in list"
        query = 'INSERT INTO emails (address, created_at) VALUES (:address, NOW())'
        mysql.query_db(query, email_data)
        session['valid'] = 'success'
        return redirect('/success')
    else:
        session['valid'] = 'fail'
        return redirect('/')

@app.route('/goback')
def goback():
    session.pop('valid')
    return redirect('/')

@app.route('/delete-entry', methods=['POST'])
def delete_entry():
    hidden_id = request.form['del_id']
    del_query = "DELETE FROM emails WHERE address = '" + hidden_id + "'"
    mysql.query_db(del_query)
    return redirect('/success')

app.run(debug=True)