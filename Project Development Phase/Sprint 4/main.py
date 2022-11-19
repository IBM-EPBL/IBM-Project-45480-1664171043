from flask import Flask, render_template, request, session, redirect

import ibm_db
import sendgrid
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


from sendgrid.helpers.mail import Mail, Email, To, Content

# clarifai
YOUR_CLARIFAI_API_KEY = "42cd5870c6934eed8774e71f597e58af"
YOUR_APPLICATION_ID = "7KH5V5-TPREJGGWJ8"
channel = ClarifaiChannel.get_json_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)

# sendgrid
SENDGRID_API_KEY = "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"

# rapid API
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/parseIngredients"
querystring = {"includeNutrition": "true"}
headers = {"content-type": "application/x-www-form-urlencoded",
            'X-RapidAPI-Key': '7a9aa3cba1msh304f811bfeb3713p15bc42jsn1c3eb4c29d4b',
            'X-RapidAPI-Host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com'
           }

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jfif'}

KEY = ""

conn = ibm_db.connect(
    "DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536"
    "=31509;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mmf10989;PWD=dyOBGeakHemxpxth",
    '', '')

print(conn)

app = Flask(__name__)

# sendgrid
def send_mail(email):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    from_email = Email("xxxxxxxxxxxxxx.foryoy@gmail.com")  # Change to your verified sender
    to_email = To(email)  # Change to your recipient
    subject = "Nutrition Application"
    content = Content("text/plain",
                      "this will made a healthier life.")
    mail = Mail(from_email, to_email, subject, content)


    mail_json = mail.get()

    response = sg.client.mail.send.post(request_body=mail_json)


def custom_send_mail(email, otp):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    from_email = Email("xxxxxxxxxx@gmail.com")  # Change to your verified sender
    to_email = To(email)  # Change to your recipient
    subject = "Easy to send mail"
    content = Content("text/plain",
                      f"OTP : '{otp}'")
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

 
    response = sg.client.mail.send.post(request_body=mail_json)
  
def generateOTP():
    digits = "348765824"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def get_history():
    history = []
    sql = f"SELECT * FROM PERSON WHERE email = '{session['email']}'"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary:
        history.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return history


def get_history_person(email):
    history = []
    sql = f"SELECT * FROM REGISTER WHERE email = '{email}'"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary:
        history.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return history


def get_history_person_time(time):
    historys = []
    sql = f"SELECT * FROM REGISTER WHERE time = '{time}'"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary:
        historys.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return historys


def get_user():
    user = []
    sql = f"SELECT * FROM USER"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary:
        user.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return user


backend = default_backend()


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST' and 'email' in request.form and 'pass' in request.form:
        error = None
        username = request.form['email']
        password = request.form['pass']
        user = None

        if username == "":
            error = 'Incorrect username.'
            return render_template('sign_in.html', error=error)

        if password == "":
            error = 'Incorrect password.'
            return render_template('sign_in.html', error=error)

        sql = "SELECT * FROM ADMIN WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            print(aes_gcm_decrypt(account['PASSWORD'], bytes(KEY, 'utf-8')))
            print(bytes(password, 'utf-8'))
            if aes_gcm_decrypt(account['PASSWORD'], bytes(KEY, 'utf-8')) == bytes(password, 'utf-8'):
                user = account['NAME']
                session["loggedIn"] = None
                session['name'] = user
                session['email'] = email
                msg = None
                history = get_history()

                list = get_user()
            return render_template('sign_in.html')

        

@app.route('/home', methods=['GET', 'POST'])
def upload_file():
    history = []
    # sql = "SELECT * FROM Students"
    sql = f"SELECT * FROM REGISTER WHERE email = '{session['email']}'"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary:
        history.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'logout' in request.form:
            session["loggedIn"] = None
            session['name'] = None
            session['password'] = None
            return render_template('index.html', error="Successfully created")
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':
            return render_template('home.html', msg="File not found", history=history)
        baseimage = file.read()
        if file and allowed_file(file.filename):
            requests = service_pb2.PostModelOutputsRequest(
            
                model_id="food-recognition",
                user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(image=resources_pb2.Image(base64=baseimage))
                    )
                ],
            )
            response = stub.PostModelOutputs(requests, metadata=metadata)

            if response.status.code != status_code_pb2.SUCCESS:
                return render_template('home.html', msg=f'Failed {response.status}', history=history)

            calcium = 0
            vitaminb5 = 0
            protein = 0
            vitamind = 0
            vitamina = 0
            vitaminb2 = 0
            carbohydrates = 0
            fiber = 0
            fat = 0
            sodium = 0
            vitaminc = 0
            calories = 0
            vitaminb1 = 0
            folicacid = 0
            sugar = 0
            vitamink = 0
            cholesterol = 0
            potassium = 0
            monounsaturatedfat = 0
            polyunsaturatedfat = 0
            saturatedfat = 0
            totalfat = 0

            calciumu = 'g'
            vitaminb5u = 'g'
            proteinu = 'g'
            vitamindu = 'g'
            vitaminau = 'g'
            vitaminb2u = 'g'
            carbohydratesu = 'g'
            fiberu = 'g'
            fatu = 'g'
            sodiumu = 'g'
            vitamincu = 'g'
            caloriesu = 'cal'
            vitaminb1u = 'g'
            folicacidu = 'g'
            sugaru = 'g'
            vitaminku = 'g'
            cholesterolu = 'g'
            potassiumu = 'g'
            monounsaturatedfatu = 'g'
            polyunsaturatedfatu = 'g'
            saturatedfatu = 'g'
            totalfatu = 'g'

            for concept in response.outputs[0].data.concepts:
                print("%12s: %.2f" % (concept.name, concept.value))
                if concept.value > 0.5:
                    payload = "ingredientList=" + concept.name + "&servings=1"
                    response1 = res.request("POST", url, data=payload, headers=headers, params=querystring)
                    data = response1.json()
                    for i in range(0, 1):
                        nutri_array = data[i]
                        nutri_dic = nutri_array['nutrition']
                        nutri = nutri_dic['nutrients']

                        for z in range(0, len(nutri)):
                            temp = nutri[z]
                            if temp['name'] == 'Calcium':
                                calcium += temp['amount']
                                calciumu = temp['unit']
                            elif temp['name'] == 'Vitamin B5':
                                vitaminb5 += temp['amount']
                                vitaminb5u = temp['unit']
                            elif temp['name'] == 'Protein':
                                protein += temp['amount']
                                proteinu = temp['unit']
                            elif temp['name'] == 'Vitamin D':
                                vitamind += temp['amount']
                                vitamindu = temp['unit']
                            elif temp['name'] == 'Vitamin A':
                                vitamina += temp['amount']
                                vitaminau = temp['unit']
                            elif temp['name'] == 'Vitamin B2':
                                vitaminb2 += temp['amount']
                                vitaminb2u = temp['unit']
                            elif temp['name'] == 'Carbohydrates':
                                carbohydrates += temp['amount']
                                carbohydratesu = temp['unit']
                            elif temp['name'] == 'Fiber':
                                fiber += temp['amount']
                                fiberu = temp['unit']
                            elif temp['name'] == 'Vitamin C':
                                vitaminc += temp['amount']
                                vitamincu = temp['unit']
                            elif temp['name'] == 'Calories':
                                calories += temp['amount']
                                caloriesu = 'cal'
                            elif temp['name'] == 'Vitamin B1':
                                vitaminb1 += temp['amount']
                                vitaminb1u = temp['unit']
                            elif temp['name'] == 'Folic Acid':
                                folicacid += temp['amount']
                                folicacidu = temp['unit']
                            elif temp['name'] == 'Sugar':
                                sugar += temp['amount']
                                sugaru = temp['unit']
                            elif temp['name'] == 'Vitamin K':
                                vitamink += temp['amount']
                                vitaminku = temp['unit']
                            elif temp['name'] == 'Cholesterol':
                                cholesterol += temp['amount']
                                cholesterolu = temp['unit']
                            elif temp['name'] == 'Mono Unsaturated Fat':
                                monounsaturatedfat += temp['amount']
                                monounsaturatedfatu = temp['unit']
                            elif temp['name'] == 'Poly Unsaturated Fat':
                                polyunsaturatedfat += temp['amount']
                                polyunsaturatedfatu = temp['unit']
                            elif temp['name'] == 'Saturated Fat':
                                saturatedfat += temp['amount']
                                saturatedfatu = temp['unit']
                            elif temp['name'] == 'Fat':
                                fat += temp['amount']
                                fatu = temp['unit']
                            elif temp['name'] == 'Sodium':
                                sodium += temp['amount']
                                sodiumu = temp['unit']
                            elif temp['name'] == 'Potassium':
                                potassium += temp['amount']
                                potassiumu = temp['unit']
                            else:
                                pass

            totalfat += saturatedfat + polyunsaturatedfat + monounsaturatedfat
            data = [calories, totalfat, saturatedfat, polyunsaturatedfat, monounsaturatedfat, cholesterol, sodium,
                    potassium, sugar, protein, carbohydrates, vitamina, vitaminc, vitamind, vitaminb5, calcium]
            unit = [caloriesu, "g", saturatedfatu, polyunsaturatedfatu, monounsaturatedfatu, cholesterolu, sodiumu,
                    potassiumu, sugaru, proteinu, carbohydratesu, vitaminau, vitamincu, vitamindu, vitaminb5u, calciumu]

            to_string = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(data[0], data[1], data[2], data[3],
                                                                                 data[4],
                                                                                 data[5], data[6], data[7], data[8],
                                                                                 data[9],
                                                                                 data[10], data[11], data[12], data[13],
                                                                                 data[14], data[15])
            current_time = strftime("%a, %d %b %Y %H:%M:%S", localtime())

            sql = "SELECT * FROM REGISTER"
            stmt = ibm_db.prepare(conn, sql)
            # ibm_db.bind_param(stmt, 1, session['password'])
            ibm_db.execute(stmt)
            # account = ibm_db.fetch_assoc(stmt)

            try:
                insert_sql = "INSERT INTO REGISTER VALUES (?,?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, session['name'])
                ibm_db.bind_param(prep_stmt, 2, session['password'])
                ibm_db.bind_param(prep_stmt, 3, to_string)
                ibm_db.bind_param(prep_stmt, 4, current_time)
                ibm_db.execute(prep_stmt)
                return render_template('home.html', user=session['name'], password=session['password'], data=data,
                                       history=history, unit=unit)
            except ibm_db.stmt_error:
                print(ibm_db.stmt_error())
                return render_template('home.html', msg='Something wnt wrong', user=session['name'],
                                       password=session['password'], data=data, history=history)

        return render_template('home.html', history=history)
    if session['name'] is None:
        return render_template('index.html')
    return render_template('home.html', user=session['name'], password=session['password'], history=history)


if __name__ == '__main__':
    app.debug = True
    app.run()
