from flask import render_template, request, make_response,jsonify
from flask import Flask
import datetime
from model import get_cust_id, med_query, add, get_med_info, get_med_det,add_model,add,reduce_medicine_qty
import json


app = Flask(__name__)


@app.route("/<cust_name>")
def bill(cust_name):
    print(cust_name)
    cust_id = get_cust_id(cust_name)
    resp = make_response(render_template("billform.html", shop_name=cust_name))
    resp.set_cookie("cust_id",cust_id)
    return resp


@app.route("/update/<cust_name>")
def update_med(cust_name):
    return render_template("update_med.html", Shop_name=cust_name)




@app.route("/search")
def search():
    medicine_name = request.args.get('medicine')
    #cust_id = request.cookies.get("cust_id")
    print(medicine_name)
    #print(cust_id)
    med_ids = med_query(medicine_name)
    if not med_ids is None:
        print(med_ids)
        med_add = add(med_ids)
        #code for checking expiry_date
        return jsonify({"status":True})
    else:
        return jsonify({"status":False})


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
    med_details,med_id = get_med_det(medicine_name, cust_id)
    final_med_data=[]
    for med_det in med_details:
        print(med_det[1])
        if not isExpired(med_det[1]):
            print("Not expired")
            obj=add_model(med_det[0],med_det[1],med_det[2],med_det[3],med_det[4],med_id)
            final_med_data.append(obj)
            print(final_med_data[0].__dict__)

    final_med_data.sort(key=lambda x:x.exp_Date,reverse=True)
    return jsonify(final_med_data[0].__dict__)


@app.route("/generate", methods=['POST'])
def generate():
    generate_bill = request.data
    bill_data=json.loads(generate_bill)
    print(bill_data)
    cust_id = request.cookies.get("cust_id")
    user_name = bill_data["username"]
    phone_number = bill_data["phone"]
    email = bill_data["email"]
    med_list = bill_data["data"]
    for med_item in med_list:
        batch_id = med_item["batch_id"]
        qty = med_item["qty"]
        reduce_medicine_qty(cust_id,batch_id,qty)
    return jsonify(json.dumps({"status":"Success"}))

if __name__ == "__main__":
    app.run(debug=False)
    #get_med_det("crocin",100)