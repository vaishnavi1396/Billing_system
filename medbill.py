from flask import render_template,request
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

@app.route("/")
def bill():
    #print("hello")
    return render_template("billform.html")

if __name__=="__main__":
    app.run()
    #bill()
