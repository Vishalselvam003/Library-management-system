from flask import*
from mysql.connector import *
import smtplib
from datetime import datetime
db = connect(host="localhost",user="root",password="vishal@9843572440",db="flask_project")
mydb=db.cursor(dictionary=True)
myapp =Flask(__name__)
myapp.secret_key='vishal'
# homepage in library
@myapp.route('/')
def home():
     return render_template("home.html") 

# adminlogin in library

@myapp.route('/adminlogin',methods=["POST","GET"]) 
def adminlogin():
    if 'admin' in request.form:
        if request.method == "POST":
            admin_name =request.form.get("adminname")
            emailid=request.form.get("adminemail")
            admin_password =request.form.get("adminpassword") 
            mydb.execute("SELECT * FROM adminlogin")
            x=mydb.fetchall()
            if x[0]['name']==admin_name and x[0]['emailid']==emailid and x[0]['password']==admin_password:
                return redirect(url_for('admin'))
            else:
                return render_template('adminlogin.html',admin="no",aname=admin_name, apass=admin_password,emailid=emailid)
    return render_template('adminlogin.html')  

# userreg in library
  
@myapp.route('/userreg',methods=["POST","GET"])
def userreg():
     if 'userreg' in request.form:
            if request.method == "POST":
                name=request.form.get('uname')
                email=request.form.get('uemail')
                mobile=request.form.get('umobile')
                password=request.form.get('upass')
                try:
                    mydb.execute("INSERT INTO users (username,email_id,mobile,password)VALUES(%s,%s,%s,%s)",(name,email,mobile,password))
                    return render_template('userreg.html',user="yes")
                except:
                    return render_template('userreg.html',user="no")
                finally:
                     db.commit()

     return render_template('userreg.html')

# userlogin in library

@myapp.route('/userlogin',methods=["POST","GET"])
def userlogin():
     if'userlogin' in request.form:
             if request.method == "POST":
                email=request.form.get('lemail')
                password=request.form.get('lpass')
                session["email"]=email
                try:
                    mydb.execute("SELECT * FROM users where email_id=%s AND password=%s",[email,password])
                    check=mydb.fetchone()
                    if check['email_id']==email and check['password']==password:
                        return render_template('user.html',name=check['username'])
                except:
                     return render_template('userlogin.html',user="no",email=email,password= password)
      
     return render_template('userlogin.html')     

# adminpage in library

@myapp.route('/adminpage')             
def admin():
    mydb.execute("SELECT * FROM books")
    book=mydb.fetchall()
    return render_template("admin.html",booklist=book)

#  view  book for admin in library

@myapp.route('/book')             
def book():
    mydb.execute("SELECT * FROM books")
    book=mydb.fetchall()
    return render_template("books.html",booklist=book)
# admin delete book 
@myapp.route('/bdelete/<string:id>',methods=["POST","GET"])             
def bdelete(id):
    mydb.execute("select * from books where book_name=%s",[id])
    bookstatus=mydb.fetchone()
    if bookstatus['book_status']=="available":
        mydb.execute("delete from books where book_name=%s",[id])
        db.commit()
        return redirect(url_for('book'))
    return redirect(url_for('book'))

# view user details in library

@myapp.route('/userdeatils')             
def userdetails():
    mydb.execute("SELECT * FROM users order by username")
    user=mydb.fetchall()
    return render_template("userdetails.html",userlist=user
    )
#admin delete user 
@myapp.route('/udelete/<string:id>',methods=["POST","GET"])             
def udelete(id):
    mydb.execute("delete from users where email_id=%s",[id])
    db.commit()
    return redirect(url_for('userdetails'))           

# edit book in library
@myapp.route('/editbook',methods=["POST","GET"])             
def editbook():
    if 'update' in request.form: 
        if request.method=="POST":
            bookname=request.form.get('bookname')
            author=request.form.get('author')
            edition=request.form.get('edition')
            publication=request.form.get("publication")
        try:
             mydb.execute("INSERT INTO books(book_name,author,book_edition,publication)VALUES(%s,%s,%s,%s)",(bookname,author,edition,publication))
             return render_template("editbook.html",book='yes')
        except:
            return render_template("editbook.html",book='no')
        finally:
            db.commit()
    return render_template("editbook.html")

# view member in library

@myapp.route('/member')              
def member():
     mydb.execute("SELECT * FROM member")
     x=mydb.fetchall()
     return render_template("member.html",member=x)

# user page in library

@myapp.route('/userpage')              
def user():
    return render_template("user.html")

#books view for user in library

@myapp.route('/bookuser')              
def bookuser():
    mydb.execute("SELECT * FROM books")
    book=mydb.fetchall()
    return render_template("bookuser.html",booklist=book)

# get book in library

@myapp.route('/getbook/<string:bookname>',methods=["POST","GET"])              
def getbook(bookname):
        return render_template('getbook.html',book=bookname)

@myapp.route('/usergetbook',methods=["POST","GET"])              
def usergetbook():
        if 'getbook' in request.form:
                if request.method == "POST":
                    bookname=request.form.get('book')
                    uname=request.form.get('name')
                    emailid=request.form.get('email')
                    mobileno=request.form.get('mobile')
                    date=request.form.get('date')
                    parsed_date = datetime.strptime(date, "%Y-%m-%d")
                    formatted_date = parsed_date.strftime("%d-%m-%Y")
                    time=request.form.get('time')
                    mydb.execute("select book_status from books where book_name=%s",[bookname])
                    bookstatus=mydb.fetchall()
                    mydb.execute("select * from  member where email=%s AND user_name=%s AND mobile=%s" ,[emailid,uname,mobileno])
                    member=mydb.fetchall()
                    mydb.execute("SELECT * FROM users where username=%s AND email_id=%s AND mobile=%s",[uname,emailid,mobileno])
                    check=mydb.fetchone()
                    status=bookstatus[0]['book_status']
                    not_available="not available"
                    if status=="available":
                        if member==[]:
                            if check:
                                mydb.execute("INSERT INTO member(user_name,book,email,mobile,booking_date,booking_time)VALUES(%s,%s,%s,%s,%s,%s)",(uname,bookname,emailid,mobileno,formatted_date,time))
                                db.commit()
                                mydb.execute("update books set book_status=%s where book_name=%s" ,[not_available,bookname])
                                db.commit() 
                                def send_email():
                                    sender_email = "vinstenvishal383@gmail.com"
                                    password = "xvmv entx arib xmll"
                                    recipient_email = emailid 
                                    subject = f"Reminder: Return {bookname} Book within 7 Days"
                                    message = f"Dear {uname},\nThank you for borrowing the {bookname} book. Please return it within 7 days.\nBest regards,\nVishal\nTHE NOVEL OASIS"

                                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                                        server.login(sender_email, password)
                                        server.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{message}")
                                        print("Mail sent successfully")

                                send_email()
  
                                return render_template('getbook.html',message="yes") 
                            else:
                                 return render_template('getbook.html',message="sorry")
                        else:
                             return render_template('getbook.html',message="no")     
                    else:
                       return render_template('getbook.html',message="not")

@myapp.route('/returnbook',methods=["POST","GET"])              
def returnbook():
           return render_template('return.html')

# return book in library

@myapp.route('/bookreturn',methods=["POST","GET"])              
def bookreturn():
     if 'returnbook' in request.form:
                if request.method == "POST":
                    bookname=request.form.get('book')
                    uname=request.form.get('name')
                    emailid=request.form.get('email')
                    available="available"
                    try:
                        mydb.execute("SELECT * FROM member where user_name=%s AND book=%s AND email=%s",[uname,bookname,emailid])
                        check=mydb.fetchone()
                        if check:
                            mydb.execute("update books set book_status=%s where book_name=%s" ,[available,bookname])
                            db.commit()
                            mydb.execute("delete from member where user_name=%s AND book=%s AND email=%s",[uname,bookname,emailid])
                            db.commit()
                            def send_email():
                                    sender_email = "vinstenvishal383@gmail.com"
                                    password = "xvmv entx arib xmll"
                                    recipient_email = emailid 
                                    subject ="Book Return Acknowledgment"
                                    message = f"Dear {uname},\nThank you for returning the book! Your promptness helps keep our library resources available for everyone's enjoyment.\nBest regards,\nVishal\nTHE NOVEL OASIS"

                                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                                        server.login(sender_email, password)
                                        server.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{message}")
                                        print("Mail sent successfully")
                            send_email()
                            return render_template('return.html',message="yes")
                        return render_template('return.html',message="no") 
                    except:
                         return render_template('return.html',message="no")        
if (__name__)=="__main__":
    myapp.run(debug=True)
