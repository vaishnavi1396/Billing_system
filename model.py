from flaskext.mysql import MySQL
from flask import Flask


app = Flask(__name__)


class add_model:
    def __init__(self, mfg_date, exp_date, cost, qty, batch_id):
        self.mfg_Date = mfg_date
        self.exp_Date = exp_date
        self.cost = cost
        self.qty = qty
        self.batch_id = batch_id


def med():
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'vaishnavi'
    app.config['MYSQL_DATABASE_DB'] = 'medicine'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    return mysql


def get_cust_id(cust_name):
    mysql = med()
    cursor = mysql.connect().cursor()
    query = """SELECT cust_id from users where uname='%s'""" % cust_name
    print(query)
    cursor.execute(query)
    cust_id = cursor.fetchone()
    print(cust_id)
    return cust_id[0]


def med_query(medicine):
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT med_id from med_det where trade_name=\'"+medicine+"\'")
    data = cursor.fetchone()
    return data


def add(sql):
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT mfg_date,exp_date,cost from med_list where med_id=\'"+sql+"\'")
    data2 = cursor.fetchone()
    return data2


def get_med_info(cust_id, trade_name):
    mysql = med()
    cursor = mysql.connect().cursor()
    print("""SELECT qty from med_acc where cust_id='%s' and med_id=(SELECT med_id from med_det where trade_name='%s')""" % (cust_id, trade_name))
    cursor.execute("""SELECT qty from med_acc where cust_id='%s' and med_id=(SELECT med_id from med_det where trade_name='%s' and det.batch_id=ac.batch_id)""" % (cust_id, trade_name))
    data = cursor.fetchone()
    print(data)
    return data[0]


def get_med_det(trade_name, cust_id):
    mysql = med()
    cursor = mysql.connect().cursor()
    print("""select med_id from med_det where trade_name='%s'""" % trade_name)
    cursor.execute("""select med_id from med_det where trade_name='%s'""" % trade_name)
    data = cursor.fetchone()
    print(data)
    if data is None:
        return None
    else:
        # for getting mfg date,exp date,cost and qty
        print("""select det.mfg_date,det.exp_date,det.cost,ac.qty from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" % (cust_id, data[0]))
        cursor.execute("""select det.mfg_date,det.exp_date,det.cost,ac.qty,det.batch_id from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" % (cust_id, data[0]))
        data = cursor.fetchall()
        print(data)
        return data


def exp(expdate):
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT batch_id from med_list where exp_date ='%s' < CURDATE()""" % expdate)
    exp_value = cursor.fetchone()
    print(exp_value)
    return exp_value
