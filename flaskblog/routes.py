from flask import render_template, url_for, flash, redirect, request
from flaskblog.models import User, Inv_Content
from flaskblog.forms import RegistrationForm, LoginForm, InventoryForm
from flaskblog import app,db,mysql
from flask_login import login_user, current_user, logout_user, login_required


#posts=[{'author':'Umair Akhtar','title':'Blog Post 1','date_posted':'12/01/2018','content':'This is Ajay hello'},{'author':'Mark T','title':'Blog post 2','date_posted':'12/01/2018','content':'This is Archana hello'}]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM inv__content")
    data = cur.fetchall()
    cur.close()
    return render_template('about.html',title='About', inv__content=data)

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html',title='Account')

@app.route("/add",methods=['GET','POST'])
def add():
    form = InventoryForm()
    if form.validate_on_submit():

        #Add from here 
        inv_content = Inv_Content(machine_name=form.machine_name.data, model=form.model.data, location=form.location.data)
        db.session.add(inv_content)
        db.session.commit()
        flash('Data has been added!','success')
        return redirect(url_for('about'))
    return render_template('add.html',title='Add',form=form)

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM inv__content WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('about'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        machine_name = request.form['machine_name']
        model = request.form['model']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE inv__content
               SET machine_name=%s, model=%s
               WHERE id=%s
            """, (name, model, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return render_template('update.html',title='Update',form=form)
