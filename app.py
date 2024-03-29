# imports
from flask import Flask, render_template, request, redirect, g
import loseit_db
import workout
import hashlib
import preference #TODO is this used


curr_user = 'Base_User'
# Define a path for the database
DATABASE_PATH = "data.sqlite"

# create a Flask app
app = Flask(__name__)

#Returns path to the database

def get_db_conn():
    if not hasattr(g, "_db_conn"):
        g._db_conn = loseit_db.initialize_db(DATABASE_PATH)
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
    global curr_user
    return render_template('CreateWorkout.html', weight = curr_user.weight)

# Create Workout Plan Page. Accessible at <server-address>/
@app.route('/viewWorkout')
def view_page():
    return render_template('ViewWorkout.html',curr_user = curr_user)

""" Todo list page. Accessible at <server-address>/todo

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
    height = request.args.get('height')
    user = request.args.get('user')
    password = request.args.get('password')
    password_hash = hashlib.md5(password.encode()).hexdigest()
    db_conn = get_db_conn()

    print(fname,lname,age,sex,weight,height,user,password)

    #Performs a function where it looks for a row that contains the user above
    #If the function returns 0 counts, prompts user that login already exists and redirect back to page with error message (define UserTaken as TRUE)
    #If user doesnt exist, redirect to createworkoutplan page
    if loseit_db.addAccount(db_conn, fname, lname, age, sex, weight, height, user, password_hash):
        global curr_user
        curr_user = loseit_db.get_user(db_conn, user, password_hash)
        return render_template('/createWorkout.html',fname = curr_user.fname, weight = curr_user.weight)
    return render_template("/createAccount.html", userTaken = True)

# Handles login task request. The task details are submitted by a HTML form with an action:
# This function extracts the inputted login and password and calls the verify_login function
@app.route('/verifyLogin', methods=['GET'])
def verifyLogin():

    #get user and password from page connection
    user = request.args.get('user')
    password = request.args.get('password')
    password_hash = hashlib.md5(password.encode()).hexdigest()
    db_conn = get_db_conn()

    #if login and password match
    if loseit_db.verifyLogin(db_conn, user, password_hash):
        global curr_user
        workoutObj = None
        curr_user = loseit_db.get_user(db_conn, user, password_hash)

        #if user already has a workout
        if curr_user.has_workout(db_conn):

            #get workout based on user a_id
            workoutObj = loseit_db.get_workout(db_conn, curr_user.id)


            #get workout exercises to print into html page
            #print image:
            # |exercise|duration|intensity|reps| x 6 exercises


            #create exercise list to be printed
            exerciseList = []

            for i in range(4):
                j = i+1
                exNum = "ex"+str(j)
                if workoutObj.workout[exNum] != None:
                    exerciseList.append(workoutObj.workout[exNum])

            #good
            print(exerciseList)

            #also add the preference data of goal and diet to the view workout template

            return render_template("/viewWorkout.html",fname = curr_user.fname, exerciseList = exerciseList,
                                   weeks=workoutObj.workout["weeks"], cal=workoutObj.workout["dfc"],
                                   days=workoutObj.workout["days"])
        else:
            return render_template("/createWorkout.html",fname = curr_user.fname, weight = curr_user.weight)

    return render_template("/main.html", failLogin=True)


@app.route('/checkAccounts')
def checkAccounts():
    loseit_db.checkAccounts(get_db_conn())
    return render_template("/main.html")

@app.route('/checkPreferences')
def checkPreferences():
    loseit_db.checkPreferences(get_db_conn())
    return render_template("/main.html")

# Handles insertion of user preferences into the database. The preferences are submitted by a HTML form with an action:

@app.route('/addPreferences', methods=['GET'])
def addPreferences():

    global curr_user
    aId = curr_user.id
    pref1 = request.args.get('pref1')
    pref2 = request.args.get('pref2')
    avoid1 = request.args.get('avoid1')
    avoid2 = request.args.get('avoid2')
    weeks = request.args.get('weeks')
    days = request.args.get('days')
    intensity = request.args.get('intensity')
    nutrition = request.args.get('nutrition')
    goal_weight = request.args.get('goal_weight')
    db_conn = get_db_conn()

    #Call database function to insert the preferences into the database
    if loseit_db.addPreferences(db_conn, aId, pref1, pref2, avoid1, avoid2, weeks, days, intensity, nutrition, goal_weight):
        return redirect("/generateWorkout") #if the user is successful in adding their preferences, it redirects to the generate workout function
    else:
        return render_template("/createWorkout.html", failPreference=True, weight = curr_user.weight)



@app.route('/generateWorkout')
def generateWorkout():
    a_id = curr_user.id

    #JUST FOR TESTING PURPOSES
    #a_id = 1

    db_conn = get_db_conn()
    e_data = loseit_db.get_exercises(db_conn)
    wo = workout.Workout(a_id)
    pref = loseit_db.get_preference(db_conn, a_id)
    wo_dic = wo.generate_workout(pref, curr_user, e_data)
    loseit_db.insert_workout(db_conn, wo_dic)
    print("Workout inserted into database")
    # create exercise list to be printed
    exerciseList = []

    for i in range(4):
        j = i + 1
        exNum = "ex" + str(j)
        if wo.workout[exNum] != None:
            exerciseList.append(wo.workout[exNum])


    return render_template("/viewWorkout.html", fname=curr_user.fname,
                           exerciseList=exerciseList, weeks = wo_dic["weeks"], cal = wo_dic["dfc"], days = wo_dic["days"])  # for now it forces to this


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
