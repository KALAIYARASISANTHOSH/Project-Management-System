from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr


database = 'database.db'

conn=sqlite3.connect(database)
cursor=conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS staff_details(Id INTEGER PRIMARY KEY AUTOINCREMENT, staff_name TEXT, staff_ID TEXT, staff_email TEXT, department TEXT, password TEXT,status TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_details(Id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, user_ID TEXT, user_email TEXT, department TEXT, password TEXT,status TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS project(Id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, project_ID TEXT, project_descrip TEXT, start_date TEXT, end_date TEXT, person_name TEXT, status INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS warning(Id INTEGER PRIMARY KEY AUTOINCREMENT, staff_name TEXT, staff_ID TEXT, staff_email TEXT, department TEXT, project_id INT, warning TEXT)")
conn.commit()

app=Flask(__name__)
@app.route("/")
@app.route("/index")
def index():
        return render_template("index.html")

@app.route("/admin", methods=['GET','POST'])
def admin():
        return render_template("admin.html")

name = 'admin'
pass_wo = 'admin'

@app.route("/adminview",methods=['POST','GET'])
def adminview():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']        
        if name == username and pass_wo == password:
                    conn=sqlite3.connect(database)
                    cursor=conn.cursor()
                    cursor.execute("select * from user_details where status=?",(0,))
                    data=cursor.fetchall()
                    cursor.execute("select * from staff_details where status=?",(0,))
                    data1=cursor.fetchall()
                    cursor.execute("select * from user_details")
                    data2=cursor.fetchall()
                    cursor.execute("select * from staff_details")
                    data3=cursor.fetchall()                
                    return render_template("adminview.html",data=data,data1=data1,data2=data2,data3=data3)
        else:            
            return render_template('admin.html', show_alert1=True)
    return render_template('admin.html')


@app.route("/approve_user",methods=['POST','GET'])
def approve_user():
    idnum=request.form['idnum']
    conn=sqlite3.connect(database)
    cursor=conn.cursor()
    cursor.execute("update user_details set status=? where Id =?",(1,idnum))
    conn.commit()    
    return render_template("adminview.html")

@app.route("/user_details",methods=['POST','GET'])
def user_details():
        if request.method == "POST":        
                user_name=request.form['user_name']
                user_ID=request.form['user_ID']
                user_email=request.form['user_email']
                department=request.form['department']
                password=request.form['password']
                conn=sqlite3.connect(database)
                cursor=conn.cursor()
                cursor.execute("insert into user_details (user_name,user_ID,user_email,department,password,status) values(?,?,?,?,?,?)",(user_name,user_ID,user_email,department,password,0))
                conn.commit()
                return render_template("index.html")
        return render_template('user_details.html')




@app.route("/user_login",methods=['POST','GET'])
def user_login():
    global user_ID
    if request.method == "POST":
            user_ID=request.form['email']
            password=request.form['password']
            conn=sqlite3.connect(database)
            cursor=conn.cursor()
            cursor.execute("select * from user_details where user_ID = ? and  password=?",(user_ID,password))
            data=cursor.fetchone()
            if data:
                cursor.execute("select * from user_details where status=? and user_ID=?",(1,user_ID))
                data1=cursor.fetchone()
                if data1:                        
                        return render_template("user_view.html")
                else:
                    return render_template('user_login.html', show_alert4=True)
            else:
                return render_template('user_login.html',show_alert1=True)

    return render_template('user_login.html')

@app.route("/user_view", methods=['POST','GET'])
def user_view():
        return render_template("user_view.html")
        


@app.template_filter('b64encode')
def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')

@app.route("/staff_details",methods=['POST','GET'])
def staff_details():
    if request.method=="POST":
        staff_name=request.form['staff_name']
        staff_ID=request.form['staff_ID']
        staff_email=request.form['staff_email']
        department=request.form['department']
        password=request.form['password']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("insert into staff_details (staff_name,staff_ID,staff_email,department,password,status) values(?,?,?,?,?,?)",(staff_name,staff_ID,staff_email,department,password,0))
        conn.commit()
        return render_template("staff_details.html",show_alert2=True)
    return render_template("staff_details.html")

@app.route("/track",methods=['POST','GET'])
def track():        
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from project")
        data = cursor.fetchall()
        conn.commit()
        return render_template("track_project.html", data = data)

@app.route("/task",methods=['POST','GET'])
def task():
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from project where status IN (?, ?, ?, ?) AND person_name = ?", (1, 5, 6, 7, user_ID,))
        data = cursor.fetchall()
        conn.commit()
        return render_template("task.html", data = data)

@app.route("/user_track",methods=['POST','GET'])
def user_track():
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from project")
        data = cursor.fetchall()
        conn.commit()
        return render_template("user_track.html", data = data)

@app.route("/warning_data",methods=['POST','GET'])
def warning_data():
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from warning")
        data = cursor.fetchall()
        conn.commit()
        return render_template("warning_data.html", data = data)

@app.route("/staff_track",methods=['POST','GET'])
def staff_track():
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from project where status=?",(0,))
        data = cursor.fetchall()
        conn.commit()
        cursor.execute("select * from user_details")
        data1 = cursor.fetchall()
        return render_template("staff_track.html", data = data, user_data = data1)
    
            
@app.route("/staff_login",methods=['POST','GET'])
def staff_login():
    if request.method=="POST":
            email=request.form['email']
            password=request.form['password']
            conn=sqlite3.connect(database)
            cursor=conn.cursor()
            cursor.execute("select * from staff_details where  staff_email= ? and  password=?",(email,password))
            data=cursor.fetchone()
            if data:
                cursor.execute("select * from staff_details where status=? and staff_email=?",(1,email))
                data1=cursor.fetchone()
                print('not work')
                if data1:
                        return render_template("staff_dashboard.html")
                else:
                    return render_template("staff_login.html",show_alert4=True)
            else:
                return render_template("staff_login.html",show_alert1=True)
    return render_template("staff_login.html")

@app.route("/staff_dashboard",methods=['POST','GET'])
def staff_dashboard():
        return render_template("staff_dashboard.html")
        


@app.route("/approve_staff",methods=['POST','GET'])
def approve_staff():
    idnum=request.form['idnum']
    conn=sqlite3.connect(database)
    cursor=conn.cursor()
    cursor.execute("update staff_details set status=? where Id =?",(1,idnum))
    conn.commit()    
    return render_template("adminview.html")


@app.route("/assign",methods=['POST','GET'])
def assign():
    if request.method == 'POST':            
            project_name=request.form['project_name']
            project_ID=request.form['project_ID']
            project_descrip=request.form['project_descrip']
            start_date=request.form['start_date']
            end_date=request.form['end_date']
            name = 'Not Assigned'
            conn=sqlite3.connect(database)
            cursor=conn.cursor()
            cursor.execute("insert into project (project_name,project_ID,project_descrip,start_date,end_date,person_name, status) values(?,?,?,?,?,?,?)",(project_name,project_ID,project_descrip,start_date,end_date,name, 0))
            conn.commit()
            return render_template("assign.html", show_alert4=True)
    return render_template("assign.html")


@app.route('/assign_project', methods=['POST'])
def assign_project():
        id1=request.form["project_id"]
        name=request.form["assigned_to"]
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("update project set person_name=?, status =? where Id =?",(name,1,id1))
        conn.commit()
        return render_template("staff_track.html", show_alert4=True)


@app.route('/task_project', methods=['POST'])
def task_project():
        id1=request.form["project_id"]
        progress=request.form["progress"]
        print(progress)
        if progress == '25':                
                conn=sqlite3.connect(database)
                cursor=conn.cursor()
                cursor.execute("update project set status =? where project_ID =?",(5,id1))
                conn.commit()
                return render_template("task.html", show_alert4=True)
        elif progress == '50':
                conn=sqlite3.connect(database)
                cursor=conn.cursor()
                cursor.execute("update project set status =? where project_ID =?",(6,id1))
                conn.commit()
                return render_template("task.html", show_alert4=True)
        elif progress == '75':
                conn=sqlite3.connect(database)
                cursor=conn.cursor()
                cursor.execute("update project set status =? where project_ID =?",(7,id1))
                conn.commit()
                return render_template("task.html", show_alert4=True)
        elif progress == '100':
                conn=sqlite3.connect(database)
                cursor=conn.cursor()
                cursor.execute("update project set status =? where project_ID =?",(2,id1))
                conn.commit()
                return render_template("task.html", show_alert4=True)
        elif progress == '1':
                conn=sqlite3.connect(database)
                cursor=conn.cursor()
                cursor.execute("update project set status =? where project_ID =?",(3,id1))
                conn.commit() 
                return render_template("task.html", show_alert4=True)


@app.route('/tasks_project', methods=['POST','GET'])
def tasks_project():
        print(user_ID)       
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from project where status IN (?, ?) AND person_name = ?", (2, 3, user_ID,))
        data2=cursor.fetchall()
        conn.commit()
        return render_template("tasks_in.html", data = data2)


@app.route("/warning",methods=['POST','GET'])
def warning():
        if request.method == 'POST':
            project_name=request.form['email']
            project_ID=request.form['subject']
            project_descrip=request.form['project_descrip']
            name=request.form['name']
            conn=sqlite3.connect(database)
            cursor=conn.cursor()
            cursor.execute("select * from user_details where user_ID=?",(name,))
            datae = cursor.fetchone()
            cursor.execute("select * from project where person_name=?",(name,))
            datat = cursor.fetchone()
            project_id = int(datat[2])
            conn=sqlite3.connect(database)
            cursor=conn.cursor()
            cursor.execute("insert into warning (staff_name,staff_ID,staff_email,department,project_id,warning) values(?,?,?,?,?,?)",(datae[1],datae[2],datae[3],datae[4],project_id,project_descrip,))
            conn.commit()
            mail = email_send(project_name,project_ID,name,project_descrip)
            return render_template("warning.html",show_alert4=True)
        return render_template("warning.html")
                


def email_send(email,subject,name,text):
            smtp_server = 'smtp.example.com'
            smtp_port = 587
            sender_email = 'diwa.2801@gmail.com'
            sender_password = 'furgqbokcooqfjkf'
            receiver_email = email
            host = "smtp.gmail.com"
            mmail = 'diwa.2801@gmail.com'      
            hmail = email
            receiver_name = name
            sender_name= "Project Manager"
            msg = MIMEMultipart()
            subject = subject
            text = text
            msg = MIMEText(text, 'plain')
            msg['To'] = formataddr((receiver_name, hmail))
            msg['From'] = formataddr((sender_name, mmail))
            msg['Subject'] = subject
            server = smtplib.SMTP(host, )
            server.ehlo()
            server.starttls()
            password = "furgqbokcooqfjkf"
            server.login(mmail, password)
            server.sendmail(mmail, [hmail], msg.as_string())
            server.quit()
            send="send"


if __name__=='__main__':
    app.run(port=350,debug=False)

    
