from flask import render_template, request,make_response
from flask import Flask
from flaskext.mysql import MySQL
import datetime

app = Flask(__name__)


@app.route("/<cust_name>")
def bill(cust_name):

    cust_id=get_cust_id(cust_name)
    resp=make_response(render_template("billform.html",shop_name=cust_name))
    resp.set_cookie("cust_id",cust_id)
    return resp


def get_cust_id(cust_name):
    mysql=med()
    cursor=mysql.connect().cursor()
    query="""SELECT cust_id from users where uname='%s'""" % cust_name
    print(query)
    cursor.execute(query)
    cust_id = cursor.fetchone()
    print(cust_id)
    return cust_id[0]


def med():
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'vaishnavi'
    app.config['MYSQL_DATABASE_DB'] = 'medicine'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    return mysql


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
    cust_id = request.cookies.get("cust_id")
    #value = "crocin"
    print(medicine_name)
    med_ids = med_query(medicine_name)
    print(med_ids)
    med_add = (add(med_ids[0]))
    print(med_add[0])
    print(med_add[1])
    print(med_add[2])
    return med_ids


def get_med_info(cust_id,trade_name):
    mysql=med()
    cursor =mysql.connect().cursor()
    print("""SELECT qty from med_acc where cust_id='%s' and med_id=(SELECT med_id from med_det where trade_name='%s')""" % (cust_id,trade_name))
    cursor.execute("""SELECT qty from med_acc where cust_id='%s' and med_id=(SELECT med_id from med_det where trade_name='%s' and det.batch_id=ac.batch_id)""" % (cust_id,trade_name))
    data = cursor.fetchone()
    print(data)
    return data[0]


def get_med_det(trade_name,cust_id):
    mysql=med()
    cursor=mysql.connect().cursor()
    print("""select med_id from med_det where trade_name='%s'""" % (trade_name))
    cursor.execute("""select med_id from med_det where trade_name='%s'""" % (trade_name))
    data=cursor.fetchone()
    print(data)
    if data is None:
        return None
    else :
        print("""select ac.qty,det.mfg_date,det.exp_date,det.cost from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" %(cust_id,data[0]))
        cursor.execute("""select ac.qty,det.mfg_date,det.exp_date,det.cost from med_acc as ac,med_list as det where ac.cust_id='%s' and ac.med_id='%s' and det.batch_id=ac.batch_id""" %(cust_id,data[0]))
        data=cursor.fetchall()
        return data[0]

@app.route("/add")
def add_medicine():
    medicine_name= request.args.get('medicine')
    cust_id=request.cookies.get("cust_id")
    data=get_med_det(medicine_name,cust_id)
    return str(data)


if __name__ == "__main__":
    app.run(debug=False)
    # get_med_det("crocin","100")
