from flask import render_template, request, make_response,jsonify
from flask import Flask
from flaskext.mysql import MySQL
import datetime
from model import add_model

app = Flask(__name__)


@app.route("/<cust_name>")
def bill(cust_name):
    print(cust_name)
    cust_id = get_cust_id(cust_name)
    resp = make_response(render_template("billform.html", shop_name=cust_name))
    resp.set_cookie("cust_id",cust_id)
    return resp


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


@app.route("/search")
def search():
    medicine_name = request.args.get('medicine')
    #cust_id = request.cookies.get("cust_id")
    print(medicine_name)
    #print(cust_id)
    med_ids = med_query(medicine_name)
    if not med_ids is None:
        print(med_ids)
        med_add = add(med_ids[0])
        #code for checking expiry_date
        return jsonify({"status":True})
    else:
        return jsonify({"status":False})




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
        #for getting mfg date,exp date,cost and qty
        print("""select det.mfg_date,det.exp_date,det.cost,ac.qty from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" % (cust_id, data[0]))
        cursor.execute("""select det.mfg_date,det.exp_date,det.cost,ac.qty,det.batch_id from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" % (cust_id, data[0]))
        data = cursor.fetchall()
        print(data)
        return data


def exp(expdate):
    mysql = med()
    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT batch_id from med_list where exp_date ='%s' < CURDATE()""" % expdate)
    exp_value=cursor.fetchone()
    print(exp_value)
    return exp_value


def isExpired(exp_date):
    currentday=datetime.date.today()
    print(currentday)
    print(currentday<exp_date)
    if exp_date < currentday:
        print("expired")
        return True
    else:
        return False

@app.route("/add")
def add_medicine():
    medicine_name = request.args.get('medicine')
    cust_id = request.cookies.get("cust_id")
    med_details = get_med_det(medicine_name, cust_id)
    final_med_data=[]
    for med_det in med_details:
        print(med_det[1])
        if not isExpired(med_det[1]):
            print("Not expired")
            obj=add_model(med_det[0],med_det[1],med_det[2],med_det[3],med_det[4])
            final_med_data.append(obj)
            print(final_med_data[0].__dict__)

    final_med_data.sort(key=lambda x:x.exp_Date,reverse=True)

    return jsonify(final_med_data[0].__dict__)


if __name__ == "__main__":
    app.run(debug=False)
    #get_med_det("crocin",100)