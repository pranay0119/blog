from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog")
with mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(username varchar(50) primary key,mobile varchar(20) unique,email varchar(50) unique,address varchar(50),password varchar(20))")
app=Flask(__name__)
app.secret_key="my secretkey is too secret"
@app.route("/")
def home():
    return "Homepage of Blog" 
@app.route("/reg",methods=['GET','POST'])
def register():  
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        Address=request.form('Address')
        Email=request.form['Email']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute("insert into registration values(%s,%s,%s,%s,%s)",(username,mobile,Address,Email,password))
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}

            return redirect(url_for('home'))
        else:
            return"Invalid username and password"
    return render_template("login.html") 
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/admin') 
def admi8n():
    return render_template('admin.html')
@app.route('/addposts')
def addposts():
    if request.method=="POST":
        title=request.form["title"]
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        corsor=mydb.cursor(buffered=True)
        cousor.execute('INSERT INTO posts(title,content,slug)VALUES(%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html') 
@app.route('/viewpost')
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select *from posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewpost.html',posts=posts)                         
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select *from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('DELETE FROM post WHERE ID=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('viewpost'))
app.run()