from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)
    
@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="insert into users(name,age,city) values (%s,%s,%s)"
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash("User Added Success!!!")
        return redirect(url_for("home"))
    return render_template("addUsers.html")
    
@app.route("/editUser/<string:id>",methods=['GET','POST'])
def editUser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        sql="update users set name=%s,age=%s,city=%s where ID=%s"
        con.execute(sql,[name,age,city,id])
        mysql.connection.commit()
        con.close()
        flash("User Updated Success!!!")
        return redirect(url_for("home"))
        con=mysql.connection.cursor()
    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editUser.html",datas=res)
    
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    flash("User Deleted Success!!!")
    return redirect(url_for("home"))
        
if(__name__=='__main__'):
    app.secret_key="mani123"
    app.run(debug=True)