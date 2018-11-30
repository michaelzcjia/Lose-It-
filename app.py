# imports
from flask import Flask, render_template, request, redirect, g
import todo_db


# Define a path for the database
DATABASE_PATH = "data.sqlite"

# create a Flask app
app = Flask(__name__)

#Returns path to the database
def get_db_conn():
    if not hasattr(g, "_db_conn"):
        g._db_conn = todo_db.initialize_db(DATABASE_PATH)
    return g._db_conn

# Welcome page. Accessible at <server-address>/
@app.route('/')
def welcome_page():
    return render_template('main.html')

# Create Account page. Accessible at <server-address>/
@app.route('/createAccount')
def account_page():
    return render_template('CreateAccount.html')

# Create Workout Plan Page. Accessible at <server-address>/
@app.route('/createWorkout')
def create_page():
    return render_template('CreateWorkout.html')

# Create Workout Plan Page. Accessible at <server-address>/
@app.route('/viewWorkout')
def view_page():
    return render_template('ViewWorkout.html')

"""" Todo list page. Accessible at <server-address>/todo

@app.route('/todo')
def todo_list():
    db_conn = get_db_conn()
    task_list = todo_db.get_tasks(db_conn)
    return render_template('todolist.html', task_list=task_list) """

# Handles account creation task. The task details are submitted by HTML Form
# This function extracts the account details and login information and calls the addAccount function to add the info into the database
@app.route('/addAccount', methods=['GET'])
def addAccount():
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    age = request.args.get('age')
    sex = request.args.get('sex')
    weight = request.args.get('weight')
    user = request.args.get('user')
    password = request.args.get('password')
    db_conn = get_db_conn()

    #Performs a function where it looks for a row that contains the user above
    #If the function returns 0 counts, prompts user that login already exists and redirect back to page with error message (define UserTaken as TRUE)
    #If user doesnt exist, redirect to createworkoutplan page
    if todo_db.addAccount(db_conn,fname,lname,age,sex,weight,user,password):
        return render_template('/viewWorkout.html')
    return render_template("/createAccount.html",userTaken = True)

# Handles login task request. The task details are submitted by a HTML form with an action:
# This function extracts the inputted login and password and calls the verify_login function
@app.route('/verifyLogin', methods=['GET'])
def verifyLogin():
    user = request.args.get('user')
    password = request.args.get('password')
    db_conn = get_db_conn()

    if todo_db.verifyLogin(db_conn,user,password):
        return render_template("/viewWorkout.html")  # for now it forces to this
    return render_template("/main.html",failLogin=True)

@app.route('/checkAccounts')
def checkAccounts():
    todo_db.checkAccounts(get_db_conn())
    return render_template("/main.html")

# Handles insertion of user preferences into the database. The preferences are submitted by a HTML form with an action:

@app.route('/addPreferences', methods=['GET'])
def addPreferences():
    #need the session variable for the user account id

    pref1 = request.args.get('pref1')
    pref2 = request.args.get('pref2')
    avoid1 = request.args.get('avoid1')
    avoid2 = request.args.get('avoid2')
    months = request.args.get('weeks')
    days = request.args.get('days')
    intensity = request.args.get('intensity')
    nutrition = request.args.get('nutrition')
    goal_weight = request.args.get('goal_weight')
    db_conn = get_db_conn()

    if todo_db.addPreferences(db_conn,pref1,pref2,avoid1,avoid2,months,days,intensity,nutrition,goal_weight):
        return render_template("/viewWorkout.html") #if the user is successful in adding their preferences, it redirects to the view of the workout
    else:
        return render_template("/createWorkout.html", failPreference=True)



# Handles add task request. The task details are submitted by a HTML form with an action="/add".
# This function extract the form field "title" and calls the app function add_task. NOTRELEVANT

@app.route('/add', methods=['GET'])
def add_task():
    task_title = request.args.get('title')
    db_conn = get_db_conn()
    task_list = todo_db.add_task(db_conn, task_title)
    return redirect("/todo", code=307)

# Handles requests to mark task as done.
# The task id of the task to be marked as done is passed using the URL, e.g., /set_done/123 is a request to mark task 123 as done.
# After the database is updated, we redirect the user back to the (updated) todo page
@app.route('/set_done/<task_id>')
def done(task_id):
    db_conn = get_db_conn()
    todo_db.set_done(db_conn, task_id)
    return redirect("/todo", code=307)

# Handles requests to mark task as not done.
# The task id of the task to be marked as not done is passed using the URL, e.g., /set_not_done/123 is a request to mark task 123 as not done.
# After the database is updated, we redirect the user back to the (updated) todo page
@app.route('/set_not_done/<task_id>')
def not_done(task_id):
    db_conn = get_db_conn()
    todo_db.set_not_done(db_conn, task_id)
    return redirect("/todo", code=307)

# Handles remove task request.
# The task id of the task to be removed is passed using the URL, e.g., /remove_task/123 is a request to remove task 123.
# After the task is removed from the database, we redirect the user back to the (updated) todo page
@app.route('/remove_task/<task_id>')
def remove_task(task_id):
    db_conn = get_db_conn()
    todo_db.remove_task(db_conn, task_id)
    return redirect("/todo", code=307)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
