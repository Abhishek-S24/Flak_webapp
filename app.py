from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Employeeinfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



#Creating model table for our CRUD database

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    empID = db.Column(db.String(100), unique=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True)
    phone = db.Column(db.String(100),unique=True)


    def __init__(self, empID, firstname,lastname, email, phone):
        self.empID = empID
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone


@app.route('/')
def comp():
    
    return render_template('entry.html')

@app.route('/enter',methods=['POST'])
def enter():
    if request.method == 'POST':
        Company_name = request.form["company_name"]
        Company_adress = request.form["company_address"]
        return render_template('menu.html')



#Route for Displaying all employee data

@app.route('/index')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)



#Route for Adding data to sqlite database via html forms


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        empID = request.form['empID']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']


        try :
            my_data = Data(empID, firstname, lastname,email,phone )
            db.session.add(my_data)
            db.session.commit()

            flash("Employee Data Inserted Successfully")

            return redirect(url_for('Index'))
        
        except:
            
            return "There was issue while adding data" 
    
    else:
        return redirect(url_for('Index'))


#This is our update route where we are going to update employee

@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        
        my_data.empID = request.form['empID']
        my_data.firstname = request.form['firstname']
        my_data.lastname = request.form['lastname']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        try:

            db.session.commit()
            flash("Employee Data Updated Successfully")

            return redirect(url_for('Index'))

        except:
            return "There was a issue while updating Employee data"

    else:
        return redirect(url_for('Index'))





#This route is for deleting  employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)

    try:
        db.session.delete(my_data)
        db.session.commit()
        flash("Employee Deleted Successfully")

        return redirect(url_for('Index'))
    
    except:
        return "There was a issue while deleting Employee data "






if __name__ == "__main__":
    app.run(debug=True)