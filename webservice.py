from flask import*



from src.dbconnection import *

app=Flask(__name__)


@app.route('/login',methods=['post'])
def login():
    print(request.form)
    username=request.form['username']
    password=request.form['password']
    qry="select*from `login` where username=%s and `password`=%s"
    val=(username,password)
    s=selectone(qry,val)

    if s is None:
        return jsonify({'task':'invalid'})
    else:
        id=s[0]
        return jsonify({'task':'valid',"id" : id })

@app.route('/register', methods=['post'])
def reg():
     try:

            firstname = request.form['Fname']
            lastname = request.form['Lname']
            age= request.form ['Age']
            gender= request.form['Gender']
            place=request.form['place']
            post=request.form['post']
            pin=request.form['pin']
            email = request.form['Email']
            contact=request.form['contact']
            username=request.form['username']
            password=request.form['password']



            qry = "INSERT INTO `login` VALUES(NULL,%s,%s,'patient')"
            val = (username,password)
            s = iud(qry, val)
            qry="insert into `patient` values(%s,Null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(str(s),firstname,lastname,age,gender,place,post,pin,email,contact)
            iud(qry,val)
            return jsonify({'task': 'success'})
     except Exception as e:
            print(e)
            return jsonify({'task': 'error'})
@app.route('/viewprofile',methods=['post'])
def viewprofile():
    userid = request.form['userid']
    qry="SELECT * FROM `patient` WHERE `lid`=%s"
    res=androidselectone(qry,userid)
    return jsonify(res)

@app.route('/updateprofile',methods=['post'])
def updateprofile():
    firstname = request.form['Fname']
    lastname = request.form['Lname']
    age = request.form['Age']
    gender = request.form['Gender']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['Email']
    contact = request.form['contact']


    qry="UPDATE `patient` SET `first name`=%s,`last name`=%s,`age`=%s,`gender`=%s,`place`=%s,`post`=%s,`pin`=%s,`email`=%s,`contact`=%s,where `patient`.`lid`=%s"
    val = (firstname,lastname,age,gender,place,post,pin,email,contact,id)


    iud(qry, val)
    return jsonify({'task': 'success'})

@app.route('/sendfeedback',methods=['post'])
def sendfeedback():
    userid=request.form['userid']
    feedback=request.form['feedback']

    qry="INSERT INTO `feedback` VALUES(NULL,%s,%s,curdate())"
    val=(userid,feedback)
    iud(qry,val)
    return jsonify({'task': 'success'})
@app.route('/senddoubt',methods=['post'])
def senddoubt():
    doubt=request.form['doubt']
    userid=request.form['userid']
    doctorid=request.form['doctorid']
    qry="INSERT INTO `doubt` VALUES(NULL,%s,%s,%s,CURDATE(),pending)"
    val=(doubt,userid,doctorid)
    iud(qry,val)
    return jsonify({'task': 'success'})
@app.route('/viewdoubtreply')
def viewdoubtreply():
    userid=request.form['userid']
    qry="SELECT * FROM `doubt` WHERE `userid`=%s"
    res=androidselectone(qry,userid)
    return jsonify(res)
@app.route('/searchdoctor')
def searchdoctor():
    specialization=request.form['specialization']
    qry="SELECT * FROM `doctor` WHERE `specialization`=%s"
    res=androidselectone(qry,specialization)
    return jsonify(res)



app.run(host="0.0.0.0",port=5000)