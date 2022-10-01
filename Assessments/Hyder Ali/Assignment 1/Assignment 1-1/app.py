from flask import Flask,request,redirect,url_for
app=Flask(__name__)
@app.route('/success/<name>')
def success(name,age,qualification):
    op="Welcome"+name+"Your email:"+email+"Number:"+number+"good luck"
    return op
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        user=request.form["nm"]
        email=request.form["email"]
        number=request.form["num"]
        return redirect(url_for('success',name = user,email = email,number = number))
if __name__=="__main__":
    app.run(debug=True)
