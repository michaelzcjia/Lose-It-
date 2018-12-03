import sqlite3
from user import User
from workout import Workout

# from preference import Preference
# Add above later when M


INITIALIZE_DB = """
	CREATE TABLE IF NOT EXISTS todo (
	 task_id INTEGER PRIMARY KEY,
	 task text NOT NULL,
	 done boolean NOT NULL default 0
	);
"""


class Task(object):
    def __init__(self, task_id, task, done):
        self.task_id = task_id
        self.task = task
        self.done = done


class Account(object):
    def __init__(self, acc_id, user, pw):
        self.acc_id = acc_id
        self.user = user
        self.pw = pw


def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute(INITIALIZE_DB)
    conn.commit()
    return conn


def verifyLogin(db_conn, user, password):
    # Returns a cursor type opject that is an iterable of tupples of rows from query
    results = db_conn.execute(
        "SELECT Username FROM Account WHERE Username = '{}' AND Password = '{}'".format(user, password))

    # Returns false is no matches for user and pass in database, true if account exists
    if results.fetchone() == None:
        return False
    else:
        return True


def checkAccounts(db_conn):
    results = db_conn.execute("SELECT * FROM ACCOUNT")
    for i in results:
        print(i)

def checkPreferences(db_conn):
    results = db_conn.execute("SELECT * FROM Preference")
    for i in results:
        print(i)

def addAccount(db_conn, fn, ln, age, sex, weight, height, user, pw):
    age2 = int(age)
    weight2 = int(weight)
    height2 = int(height)
    count = db_conn.execute("SELECT COUNT(*) FROM ACCOUNT")
    try:
        count = count.fetchone()
    except:
        count = 0
    try:  # Added height after weight
        statement = "INSERT INTO ACCOUNT (a_id, first_name, last_name,age,sex,weight,height,username,password,maintenance) " \
                    "VALUES ('{}','{}','{}',{},'{}',{},'{}','{}',{})".format(count, fn, ln, age2, sex, weight2, height2,
                                                                             user, pw, 123)
        db_conn.execute(statement)
        db_conn.commit()
    except Exception:
        return False
    return True


def get_user(db_conn, user, password):
    fill = (user, password,)
    results = db_conn.execute('SELECT * FROM ACCOUNT WHERE USERNAME = ? AND PASSWORD = ?', fill)
    curr_user = User(results.fetchone())
    return curr_user


# This function inserts the users entered preferences into the account
# I don't think pId is needed, if there are already account preferences for an account we can just update them.

def addPreferences(db_conn, aId, p1, p2, a1, a2, weeks, days, intensity, nutrition, goalWeight):
    weight2 = int(goalWeight)
    weeks2 = int(weeks)
    days2 = int(days)
    resultSet = db_conn.execute("SELECT * FROM Preference WHERE A_ID = ?", aId)  # determine if there are already preferences
    print("Aid ",aId)
    print(resultSet)
    if(resultSet.fetchone()):
        count = 1
    else:
        count = 0
    try:  # If there are no preferences for the current user, then insert the preferences into the database
        if (count == 0):
            statement = "INSERT INTO Preference (A_ID, Pref1, Pref2, Avoid1, Avoid2,Weeks, Days, Intensity,Nutrition, \
			Goal_weight) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(aId, p1, p2, a1, a2, weeks2, days2, intensity, nutrition, weight2)
            db_conn.execute(statement)
            db_conn.commit()
        else:  # If there are existing preferences, then we will update the values
            statement = "UPDATE Preference SET Pref1 = '{}', Pref2 = '{}', Avoid1 = '{}', Avoid2 = '{}',\
			Weeks = '{}', Days = '{}', Intensity = '{}', Nutrition = '{}', Goal_weight = '{}' WHERE A_ID = '{}'" \
                .format(p1, p2, a1, a2, weeks2, days2, intensity, nutrition, weight2, aId)
            db_conn.execute(statement)
            db_conn.commit()
    except Exception:
        return False
    return True

# Task Functions below

def get_tasks(db_conn):
    results = db_conn.execute("SELECT task_id, task, done FROM todo;")

    task_list = []
    for task_id, task, done in results:
        current_task = Task(task_id, task, done)
        task_list.append(current_task)

    return task_list


def add_task(db_conn, task):
    if not task:
        return
    sqlInsert = "INSERT INTO todo (task, done) VALUES ('{}', 0)".format(task)
    db_conn.execute(sqlInsert)
    db_conn.commit()


def insert_random(db_conn):
    print("@@@@@@@@@@")
    sqlInsert = "INSERT INTO Account (a_id, first_name, last_name,age,sex,weight,username,password,maintenance)" \
                "values ('00000001','first','last',5,'M','10','user','pass','123')"
    db_conn.execute(sqlInsert)
    db_conn.commit()


def set_done(db_conn, task_id):
    sqlUpdate = "UPDATE todo SET done=1 WHERE task_id={}".format(task_id)
    db_conn.execute(sqlUpdate)
    db_conn.commit()


def set_not_done(db_conn, task_id):
    sqlUpdate = "UPDATE todo SET done=0 WHERE task_id={}".format(task_id)
    db_conn.execute(sqlUpdate)
    db_conn.commit()


def remove_task(db_conn, task_id):
    sqlDelete = "DELETE FROM todo WHERE task_id={}".format(task_id)
    db_conn.execute(sqlDelete)
    db_conn.commit()


def printWorkout(db_conn):
    sql = "SELECT * FROM Workout"
    results = db_conn.execute(sql)
    for i in results:
        print(i)
    print("printed")


def get_workout(db_conn, a_id):
    sqlSelect = "SELECT * from Workout WHERE A_ID = '{}'".format(a_id)

    results = db_conn.execute(sqlSelect)
    workout_data = results.fetchone()
    print(workout_data)

    if workout_data == None:
        print('what the fucc')
        return False
    else:
        print("should be ok")
        workout = Workout(workout_data)
        return workout


# Pulls preference information from database to return a Preference object
def get_preference(db_conn, a_id):
    sqlSelect = "SELECT * from Preference WHERE A_ID = '{}'".format(a_id)

    results = db_conn.execute(sqlSelect)
    preference_data = results.fetchone()
    print(preference_data)

    if preference_data == None:
        print('it really do be like that sometimes')
        return False
    else:
        print("Preferences are litty fams")
        preference = Preference(preference_data)
        return preference
