from flask import *
from src.dbconnection import *
app=Flask(__name__)
app.secret_key="1234"
import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return '''<script>alert("please login");window.location='login1'</script>'''

        return func()

    return secure_function

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/loog')
def loog():
    return render_template("LOGIN.html")




@app.route('/addandmanagedoctor')
@login_required
def add():
    qry="select * from doctor"
    res=select(qry)
    return render_template("add and manage doctor.html",val=res)

@app.route('/deletedoctor')
@login_required
def deletedoctor():
    id=request.args.get('id')
    qry="DELETE FROM `doctor` WHERE lid=%s"
    iud(qry,id)
    return'''<script>alert("deleted");window.location='addandmanagedoctor'</script>'''


@app.route('/editdoctor')
@login_required
def editdoctor():
    id = request.args.get('id')
    session['docid'] = id
    qry = "SELECT * FROM `doctor` WHERE lid=%s"
    res = selectone(qry, str(id))
    return render_template("EDIT DOCTOR.html",val=res)




@app.route('/updatedoctor',methods=['post'])
@login_required
def updatedoctor():
    id = session['docid']
    firstname = request.form['textfield1']
    lastname=request.form['textfield2']
    age=request.form['textfield3']
    gender=request.form['radiobutton']
    specialization=request.form['textfield4']
    place=request.form['textfield5']
    post=request.form['textfield6']
    pin=request.form['textfield7']
    email=request.form['textfield8']
    phone=request.form['textfield9']

    qry="UPDATE `doctor` SET `first name`=%s,`last name`=%s,`age`=%s,`gender`=%s,`specialization`=%s,`contact`=%s,`e mail`=%s,`place`=%s,`post`=%s,`pin`=%s where `doctor`.`lid`=%s"
    val = (firstname,lastname,age,gender,specialization,phone,email,place,post,pin,id)
    iud(qry, val)
    return '''<script>alert("updated");window.location='addandmanagedoctor'</script>'''


@app.route('/adddisease',methods=['post'])
@login_required
def adddisease():
    return render_template("ADD DIS.html")
@app.route('/add2',methods=['post'])
@login_required
def add2():
    return render_template("ADD DOCTOR.html")
@app.route('/addnmandis')
@login_required
def add3():
    qry="select * from disease"
    res=select(qry)

    return render_template("add n man dis.html",val=res)

@app.route('/deletedisease')
@login_required
def deletedisease():
    id=request.args.get('id')
    qry="DELETE FROM `disease` WHERE `id`=%s"
    iud(qry,id)
    return '''<script>alert("deleted");window.location='addnmandis'</script>'''

@app.route('/editdisease')
@login_required
def editdisease():
    id=request.args.get('id')
    session['did']=id
    qry="SELECT * FROM `disease` WHERE `id`=%s"
    res=selectone(qry,str(id))
    return render_template("EDIT DIS.html",val=res)
@app.route('/updatedisease',methods=['post'])
@login_required
def updatedisease():
    id=session['did']
    disease = request.form['textfield']
    description = request.form['textarea']
    qry="UPDATE `disease` SET `disease`=%s , `description`=%s WHERE `id`=%s"
    val=(disease,description,id)
    iud(qry,val)
    return '''<script>alert("updated");window.location='addnmandis'</script>'''


@app.route('/admhome')
@login_required
def add4():
    return render_template("ADM HOME.html")
@app.route('/dochome')
@login_required
def add5():
    return render_template("DOC HOME.html")
@app.route('/rep')
@login_required
def add6():
    id = request.args.get('id')
    session['cid']=id
    return render_template("REP.html")

@app.route('/sendreply',methods=['post'])
@login_required
def sendreply():

    reply = request.form['textfield']
    qry="UPDATE `doubt` SET `reply`=%s WHERE `doubtid`=%s"
    val=(reply,session['cid'])
    iud(qry,val)
    return'''<script>alert("successfull");window.location='rep'</script>'''



@app.route('/userdoubt')
@login_required
def userdoubt():
    did=session['lid']
    qry="SELECT `doubt`.*,`patient`.`firstname`,`patient`.`lastname` FROM `patient` JOIN `doubt` ON `doubt`.`userid`=`patient`.`lid` JOIN `doctor` ON `doctor`.`lid`=`doubt`.`doctorid` WHERE `doubt`.`reply`='pending' AND `doubt`.`doctorid`=%s"
    res=selectall(qry,did)
    return render_template("USER DOUBT N REP.html",val=res)
@app.route('/viewf')
@login_required
def viewf():
    qry="SELECT `feedback`.*,`patient`.`firstname`,`patient`.`lastname` FROM `patient` JOIN `feedback` ON `feedback`.`userid`=`patient`.`lid`"
    res=select(qry)

    return render_template("view feed.html",val=res)
@app.route('/viewpat1')
@login_required
def viewpat1():
    qry="SELECT * FROM `patient`"
    res=select(qry)
    return render_template("VIEW PAT.html",val=res)
@app.route('/viewpat2')
@login_required
def viewpat2():
    qry = "SELECT * FROM `patient`"
    res = select(qry)

    return render_template("viewpat.html",val=res)


@app.route('/login1',methods=['post'])

def login1():
    uname=request.form['textfield']
    pswd=request.form['textfield2']
    qry="select * from login where username=%s and password=%s"
    val=(uname,pswd)
    res=selectone(qry,val)
    if res is None:
        return '''<script>alert("invalid password or username");window.location='/'</script>'''
    elif res[3]=='admin':
        session['lid'] = res[0]
        return '''<script>alert("welcome");window.location='admhome'</script>'''
    elif res[3]=='doctor':
        session['lid']=res[0]
        return '''<script>alert("welcome");window.location='dochome'</script>'''

@app.route('/adddoctor',methods=['post'])
@login_required
def adddoctor():
    try:
        firstname=request.form['textfield1']
        lastname=request.form['textfield2']
        age=request.form['textfield3']
        gender=request.form['radiobutton']
        specialization=request.form['textfield4']
        place=request.form['textfield5']
        post=request.form['textfield6']
        pin=request.form['textfield7']
        email=request.form['textfield8']
        phone=request.form['textfield9']
        uname=request.form['textfield10']
        passwd=request.form['textfield11']

        qry="insert into login values(NULL,%s,%s,'doctor')"
        val=(uname,passwd)
        id=iud(qry,val)
        qry="insert into doctor values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(str(id),firstname,lastname,age,gender,specialization,phone,email,place,post,pin)
        iud(qry,val)


        return '''<script>alert("success");window.location='addandmanagedoctor'</script>'''
    except Exception as e:
        return '''<script>alert("dupicate entry,please try again");window.location='addandmanagedoctor'</script>'''


@app.route('/adddisease1', methods=['post'])
@login_required
def adddisease1():
    disease=request.form['textfield']
    description=request.form['textarea']


    qry="insert into disease values(NULL,%s,%s)"
    val=(disease,description)
    iud(qry,val)
    return '''<script>alert("success");window.location='addnmandis'</script>'''


@app.route('/logout')
def logout():
    session.clear()
    return render_template("LOGIN.html")


app.run(debug=True)



















































app.run(debug=True)




