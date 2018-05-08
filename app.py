from flask import render_template, request, make_response, jsonify
from flask import Flask
import datetime
from model import *
import json
import smtplib
import requests

from uitemplates import text_template_class
token = "EAACGHzJZBmDABAOlZAEPVM2ikVWHx8hlMzmTZCO6l3s3kWMjQo5oywc0H8NK3IfMehFoEIHRS4W0w6REcfKWzxy7P9qAayTZBeVVZCpcU7KdSbC4rhiZBYMMryYLZCf0QEmEJSBqNSEZBJy7fEQmT7MQdoWYqTLEZBJOxKgkrioYhqv1AYTORC8Uu"


app = Flask(__name__)


@app.route("/<cust_name>")
def bill(cust_name):
    print(cust_name)
    cust_id = get_cust_id(cust_name)
    resp = make_response(render_template("billform.html", shop_name=cust_name))
    resp.set_cookie("cust_id", cust_id)
    return resp


@app.route("/update/<cust_name>")
def update_med(cust_name):
    print(cust_name)
    cust_id = get_customer_id(cust_name)
    result = make_response(render_template("update_med.html", Shop_name=cust_name))
    result.set_cookie("cust_id", cust_id)
    return result


@app.route("/search")
def search():
    medicine_name = request.args.get('medicine')
    cust_id = request.cookies.get("cust_id")
    # print(medicine_name)
    # print(cust_id)
    med_ids = medicine_id_search(cust_id, medicine_name)
    if not med_ids is None:
        #print(med_ids)
        # med_add = add(med_ids)
        return jsonify({"status":True})
    else:
        return jsonify({"status":False})


def isExpired(exp_date):
    currentday = datetime.date.today()
    print(currentday)
    print(currentday < exp_date)
    if exp_date < currentday:
        print("expired")
        return True
    else:
        return False





@app.route("/add")
def add_medicine():
    medicine_name = request.args.get('medicine')
    cust_id = request.cookies.get("cust_id")
    med_details, med_id = get_med_det(medicine_name, cust_id)
    final_med_data = []
    for med_det in med_details:
        print(med_det[1])
        if not isExpired(med_det[1]):
            print("Not expired")
            obj = add_model(med_det[0], med_det[1], med_det[2], med_det[3], med_det[4], med_id)
            final_med_data.append(obj)
            print(final_med_data[0].__dict__)
    final_med_data.sort(key=lambda x:x.exp_Date, reverse=True)
    return jsonify(final_med_data[0].__dict__)


def reduce_medicine_qty(cust_id,batch_id,qty):
    user_qty = qty
    updated_qty_value = remove_qty(user_qty,batch_id)
    return updated_qty_value



def reply(data):
    json_data = json.dumps(data)
    print("What is this json data")
    print(json_data)
    req = requests.post("https://graph.facebook.com/v2.6/me/messages",params={"access_token": token}, \
                        headers={"Content-Type": "application/json"},data=json_data)
    print(req.content)



def send_bill_information(cust_id,mydict,**kwargs):
    # mydict={'username': 'vivek', 'phone': '8088432316', 'email': 'vivekstarstar', 'data': [{'batch_id': 'p302', 'qty': '1', 'med_id': '202'}, {'batch_id': 'p302', 'qty': '1', 'med_id': '202'}]}

    phone_number = mydict['phone']
    shop_name=get_shop_name(cust_id)

    recipient_id = search_by_phone(phone_number)

    text="Hey thanks for billing at "+shop_name+"! Following is your bill information \n"
    display_bill = []
    total_cost=0
    for medicine in mydict['data']:
        batch_id=medicine['batch_id']
        med_id=medicine['med_id']
        (mfg,exp,cost) = get_med_data(batch_id,med_id)
        drug,trade=get_drug_trade(med_id)
        qty=medicine["qty"]
        tcost=int(qty)*int(cost)
        temp="tablate:"+trade+",qty:"+qty+",cost:"+str(tcost)+",exp:"+str(exp)+"\n"
        total_cost+=tcost
        text+=temp
    text+="total cost:"+str(total_cost)+"\n"
    print(text)
    if not recipient_id is None:
        data = text_template_class(recipient_id,text,subscription_message=True).__dict__
        print(data)
        reply(data)
    else:
        # Todo:send mail to this new user
        gmail_user = ''
        gmail_password = ''
        #TODO: how to get email of this customer
        customer_email = mydict['email']
        sent_from = gmail_user
        to = [customer_email]
        subject = 'Medicine Bot to share medicines!'
        body = "Dear Customer,\nIf you would like to share the extra medicines bought by you now, kindly like our" \
               "facebook page, In Zone drug remedy\n" \
               "Thanks!"

        email_text = """\  
        %s
        """ % (sent_from, ", ".join(to), subject, body)
        message = 'Subject: {}\n\n{}'.format(subject, email_text)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, message)
            server.close()

            print('Email sent!')
        except:
            print('Something went wrong...')


@app.route("/generate", methods=['POST'])
def generate():
    generate_bill = request.data
    bill_data = json.loads(generate_bill)
    print(bill_data)
    cust_id = request.cookies.get("cust_id")
    user_name = bill_data["username"]
    phone_number = bill_data["phone"]
    email = bill_data["email"]
    med_list = bill_data["data"]
    for med_item in med_list:
        batch_id = med_item["batch_id"]
        qty = med_item["qty"]
        reduce_medicine_qty(cust_id, batch_id,qty)
    send_bill_information(cust_id,bill_data)
    return jsonify(json.dumps({"status ": "Success"}))


@app.route("/med_update", methods=['POST'])
def med_update():
    cust_id = request.cookies.get("cust_id")
    med_name = request.form['mname']
    trade_name = request.form['tname']
    batch_id = request.form['batch_id']
    mfg_date = request.form['mfg']
    exp_date = request.form['exp']
    cost = request.form['cost']
    quantity = request.form['qty']
    description = request.form['desc']
    print(med_name, trade_name, batch_id, mfg_date, exp_date, cost, quantity, description, cust_id)
    medicine_id = medicine_query(trade_name)
    print(medicine_id)
    if medicine_id is None:
        insert_medicine(med_name, trade_name, batch_id, mfg_date, exp_date, cost, quantity, description, cust_id)
    medi_id = med_query(trade_name)
    if not medi_id is None:
        medicine_update(quantity, medi_id)
    return render_template("update_success.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)
