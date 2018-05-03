from flaskext.mysql import MySQL
from flask import Flask


app = Flask(__name__)


class add_model:
    def __init__(self, mfg_date, exp_date, cost, qty, batch_id,med_id):
        self.mfg_Date = mfg_date
        self.exp_Date = exp_date
        self.cost = cost
        self.qty = qty
        self.batch_id = batch_id
        self.med_id=med_id


def med():
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_DB'] = 'medicine'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    return mysql


def get_cust_id(cust_name):
    mysql = med()
    cursor = mysql.connect().cursor()
    query = """SELECT cust_id from users where uname='%s'""" % cust_name
    #print(query)
    cursor.execute(query)
    cust_id = cursor.fetchone()
    print(cust_id)
    return cust_id[0]


def med_query(medicine):
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT med_id from med_det where trade_name=\'"+medicine+"\'")
    data = cursor.fetchone()
    print(data)
    return data


def add(med_id):
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT mfg_date,exp_date,cost from med_list where med_id=\'"+med_id+"\'")
    med_info = cursor.fetchone()
    return med_info


def get_med_qty(cust_id, trade_name):
    mysql = med()
    cursor = mysql.connect().cursor()
    print("""SELECT qty from med_acc where cust_id='%s' and med_id=(SELECT med_id from med_det where trade_name='%s')""" % (cust_id, trade_name))
    cursor.execute("""SELECT qty from med_acc where cust_id='%s' and med_id=(SELECT med_id from med_det where trade_name='%s' and det.batch_id=ac.batch_id)""" % (cust_id, trade_name))
    data = cursor.fetchone()
    print(data)
    return data[0]


# for getting mfg date,exp date,cost,qty and batch_id
def get_med_info(cust_id,med_id):
    mysql = med()
    cursor = mysql.connect().cursor()
    print("""select det.mfg_date,det.exp_date,det.cost,ac.qty from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" % (cust_id, med_id))
    cursor.execute("""select det.mfg_date,det.exp_date,det.cost,ac.qty,det.batch_id from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" % (cust_id, med_id))
    med_info = cursor.fetchall()
    print(med_info)
    return med_info


def get_med_det(trade_name, cust_id):
    cust_ID = cust_id
    med_id = med_query(trade_name)
    print(med_id)
    if med_id is None:
        return None
    else:
        med_det = get_med_info(cust_ID,med_id)
    return med_det,med_id


def exp(expdate):
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT batch_id from med_list where exp_date ='%s' < CURDATE()""" % expdate)
    exp_value = cursor.fetchone()
    print(exp_value)
    return exp_value


def remove_qty(user_qty,cust_id):
    mysql = med()
    db = mysql.connect()
    cursor = db.cursor()
    print("""update med_acc set qty = qty - %s where cust_id='%s' """ % (user_qty,cust_id))
    cursor.execute("""update med_acc set qty = qty - %s where cust_id='%s' """ % (user_qty,cust_id))
    db.commit()
    db.close()


def med_id_gen():
    with open("med_id_generation.txt","r") as f:
        last_med_id = f.readline()
    print(last_med_id)
    new_med_id = (abs(hash(last_med_id)))
    with open("med_id_generation.txt","w") as f:
        f.write(str(new_med_id))
    print(new_med_id)
    return str(new_med_id)


def insert_query_drug(med_name, trade_name):
    mysql = med()
    db = mysql.connect()
    cursor=db.cursor()
    print("""insert into drug values(%s,%s)"""%((med_name,trade_name)))
    cursor.execute("""insert into drug values('%s','%s')"""%(med_name,trade_name))
    db.commit()
    db.close()


def insert_query_med_det(medicine_id, med_name, description, trade_name):
    mysql = med()
    db = mysql.connect()
    cursor=db.cursor()
    print("""insert into med_det values('%s','%s','%s','%s')"""%(medicine_id, med_name, description, trade_name))
    cursor.execute("""insert into med_det values('%s','%s','%s','%s')"""%(medicine_id, med_name, description, trade_name))
    db.commit()
    db.close()


def insert_query_med_acc(cust_id, med_id, batch_id, qty):
    mysql = med()
    db=mysql.connect()
    cursor=db.cursor()
    print("""insert into med_acc values('%s','%s','%s','%d')"""%(cust_id, med_id, batch_id, qty))
    cursor.execute("""insert into med_acc values('%s','%s','%s','%d')"""%(cust_id, med_id, batch_id, qty))
    db.commit()
    db.close()


def insert_query_med_list(batch_id, medicine_id, mfg_date, exp_date, cost):
    mysql = med()
    db = mysql.connect()
    cursor=db.cursor()
    print("""insert into med_list values('%s','%s','%s','%s','%s')"""  %(batch_id, medicine_id,mfg_date, exp_date, cost))
    cursor.execute("""insert into med_list values('%s','%s','%s','%s','%s')""" % (batch_id, medicine_id, mfg_date, exp_date, cost))
    db.commit()
    db.close()


def insert_medicine(med_name,trade_name, batch_id, mfg_date, exp_date, cost, quantity, description, cust_id):
    insert_query_drug(med_name,trade_name)
    medicine_id = med_id_gen()
    insert_query_med_det(medicine_id, med_name, description, trade_name)
    insert_query_med_list(batch_id, medicine_id, str(mfg_date), str(exp_date), cost)
    insert_query_med_acc(cust_id, medicine_id, batch_id, int(quantity))


def update_qty(qty,cust_id):
    mysql = med()
    db = mysql.connect()
    cursor = db.cursor()
    print("""update med_acc set qty = qty + %s where cust_id='%s' """ % (qty,cust_id))
    cursor.execute("""update med_acc set qty = qty + %s where cust_id='%s' """ % (qty,cust_id))
    db.commit()
    db.close()


def medicine_update(qty,cust_id):
    mysql = med()
    db = mysql.connect()
    cursor = db.cursor()
    print("""update med_acc set qty = qty + %s where cust_id='%s' """ % (qty, cust_id))
    cursor.execute("""update med_acc set qty = qty + %s where cust_id='%s' """ % (qty, cust_id))
    db.commit()
    db.close()

