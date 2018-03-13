from flask import render_template,request
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

@app.route("/bill/<name>")
def bill(name):
    return render_template("billformat.html")


def med():
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'vaishnavi'
    app.config['MYSQL_DATABASE_DB'] = 'medicine'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    return mysql

def med_query(medicine):
    mysql=med()
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT med_id from med_det where trade_name=\'"+medicine+"\'")
    data = cursor.fetchone()
    return data
g
def exp():
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT batch_id from med_list where exp_date < CURDATE()")
    data1=cursor.fetchone()
    print(data1)

@app.route("/search")
def ajax():
    value =str(request.args.get('medicine'))
    print(value)
    sql = med_query(value)
    print(sql)
    return sql


if __name__=="__main__":
    app.run(debug=False)
    #ajax()