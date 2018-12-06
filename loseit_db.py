import sqlite3
from user import User
from workout import Workout
from preference import Preference

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


def addAccount(db_conn, fn, ln, age, sex, weight, height, user, pw):
    sex2 = 'M' if sex == 'Male' else 'F'
    age2 = int(age)
    weight2 = float(weight)
    height2 = float(height)
    count = db_conn.execute("SELECT COUNT(*) FROM ACCOUNT")
    try:
        count = count.fetchone()
    except:
        count = 0
    available = db_conn.execute("SELECT COUNT(*) FROM ACCOUNT WHERE username = '{}'".format(user))

    if(available.fetchone()[0] != 0):
        return False
    try:  # Added height after weight
        statement = "INSERT INTO ACCOUNT (a_id, first_name, last_name, age, sex, weight, height, username, password, maintenance) " \
                    "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(count[0], fn, ln, age2, sex2,
                                                                                        weight2, height2, user, pw, 123)
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


def checkPreferences(db_conn):
    results = db_conn.execute("SELECT * FROM Preference")
    for i in results:
        print(i)


# This function inserts the users entered preferences into the account
# I don't think pId is needed, if there are already account preferences for an account we can just update them.

def addPreferences(db_conn, aId, p1, p2, a1, a2, weeks, days, intensity, nutrition, goalWeight):
    weight2 = float(goalWeight)
    weeks2 = float(weeks)
    days2 = int(days)
    resultSet = db_conn.execute(
        "SELECT * FROM Preference WHERE A_ID = '{}'".format(aId))  # determine if there are already preferences
    if (resultSet.fetchone()):
        count = 1
    else:
        count = 0
    try:  # If there are no preferences for the current user, then insert the preferences into the database
        if (count == 0):
            statement = "INSERT INTO Preference (A_ID, Pref1, Pref2, Avoid1, Avoid2,Weeks, Days, Intensity,Nutrition, \
			Goal_weight) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(aId, p1, p2, a1, a2, weeks2,
                                                                                            days2, intensity, nutrition,
                                                                                            weight2)
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


def printWorkout(db_conn):
    sql = "SELECT * FROM Workout"
    results = db_conn.execute(sql)
    for i in results:
        print(i)


def get_workout(db_conn, a_id):
    sqlSelect = "SELECT * from Workout WHERE A_ID = '{}'".format(a_id)

    results = db_conn.execute(sqlSelect)
    workout_data = results.fetchone()
    print(workout_data)

    if workout_data == None:
        return False
    else:
        workout_plan = Workout(workout_data)
        return workout_plan


# Pulls preference information from database to return a Preference object
def get_exercises(db_conn):
    sqlSelect = "SELECT * from Exercise"

    results = db_conn.execute(sqlSelect)
    data = results.fetchall()
    return data


def get_preference(db_conn, a_id):
    sqlSelect = "SELECT * from Preference WHERE A_ID = '{}'".format(a_id)

    results = db_conn.execute(sqlSelect)
    preference_data = results.fetchone()
    print(preference_data)

    if preference_data == None:
        return False
    else:
        preference = Preference(preference_data)
        return preference


def insert_workout(db_conn, d):

    #Delete any existing workouts

    try:
        sqlDelete = "DELETE FROM Workout WHERE A_ID = '{}'".format(d['a_id'])
        db_conn.execute(sqlDelete)
        db_conn.commit()
    #The print is just to get the code to continue working
    except:
        print("")
    sqlInsert = "INSERT INTO Workout (W_ID, A_ID, Exercise1, Duration1, Intensity1, Desc1, Link1," \
                "Exercise2, Duration2, Intensity2, Desc2, Link2," \
                "Exercise3, Duration3, Intensity3, Desc3, Link3," \
                "Exercise4, Duration4, Intensity4, Desc4, Link4," \
                "Days,Weeks,Maintenance, Deficit) " \
                "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                "'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(d['id'], d['a_id'],
                                                                                 d['ex1']['ex'], d['ex1']['dur'],
                                                                                 d['ex1']['int'], d['ex1']['descr'],
                                                                                 d['ex1']['img'],
                                                                                 d['ex2']['ex'], d['ex2']['dur'],
                                                                                 d['ex2']['int'], d['ex2']['descr'],
                                                                                 d['ex2']['img'],
                                                                                 d['ex3']['ex'], d['ex3']['dur'],
                                                                                 d['ex3']['int'], d['ex3']['descr'],
                                                                                 d['ex3']['img'],
                                                                                 d['ex4']['ex'], d['ex4']['dur'],
                                                                                 d['ex4']['int'], d['ex4']['descr'],
                                                                                 d['ex4']['img'],
                                                                                 d['days'], d['weeks'], d['mnt'],
                                                                                 d['dfc'])
    db_conn.execute(sqlInsert)
    db_conn.commit()

def check_workout(db_conn, aId):
    '''Checks if there is a workout for the account, returns True if workout present'''

    statement = "SELECT COUNT(*) FROM Workout WHERE A_ID = '{}'".format(aId)
    result = db_conn.execute(statement)
    if (result.fetchone()[0] == 0):
        return False
    else:
        return True
