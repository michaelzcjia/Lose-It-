import sqlite3


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

def verifyLogin(db_conn,user,password):
	#Returns a cursor type opject that is an iterable of tupples of rows from query
	results = db_conn.execute("SELECT Username FROM Account WHERE Username = '{}' AND Password = '{}'".format(user,password))

	#Returns false is no matches for user and pass in database, true if account exists
	if results.fetchone() == None:
		return False
	else:
		return True

def checkAccounts(db_conn):
	results = db_conn.execute("SELECT * FROM ACCOUNT")
	for i in results:
		print(i)

def addAccount(db_conn,fn,ln,age,sex,weight,user,pw):
	age2 = int(age)
	weight2 = int(weight)
	count = db_conn.execute("SELECT COUNT(*) FROM ACCOUNT")
	try:
		count = count.fetchone()
	except:
		count = 0
	try:
		statement = "INSERT INTO ACCOUNT (a_id, first_name, last_name,age,sex,weight,username,password,maintenance) " \
					"VALUES ('{}','{}','{}',{},'{}',{},'{}','{}',{})".format(count,fn,ln,age2,sex,weight2,user,pw,123)
		db_conn.execute(statement)
		db_conn.commit()
	except Exception:
		return False
	return True

#This function inserts the users entered preferences into the account
#I don't think pId is needed, if there are already account preferences for an account we can just update them.

def addPreferences(db_conn,aId, p1, p2, p3, a1, a2, a3, weeks, days, intensity, minutes, nutrition, goalWeight):
	weeks2 = int(weeks)
	days2 = int(days)
	resultSet = db_conn.execute("SELECT COUNT(*) FROM ACCOUNT WHERE A_ID = '{}'".format(aId)) #determine if there are already preferences
	try:
		count = resultSet.fetchone()
	except:
		count = 0
	try:
		if(count == 0):
			statement = "INSERT INTO Preference (A_id, Pref1, Pref2, Avoid1, Avoid2,Weeks, Days, Intensity, Minutes, Nutrition, \
						Goal_weight)"  "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
						.format(aId,p1,p2,a1,a2,weeks2,days,intensity,nutrition,goalWeight)
			db_conn.execute(statement)
			db_conn.commit()
		else:
			# Update the preferences instead of inserting new ones
			statement = "UPDATE Preference SET Pref1 = '{}', Pref2 = '{}', Avoid1 = '{}', Avoid2 = '{}',\
						Weeks = '{}', Days = '{}', Intensity = '{}', Nutrition = '{}', Goal_weight = '{}' WHERE A_Id = '{}'"\
						.format(p1,p2,a1,a2,weeks2,days,intensity,nutrition,goalWeight,aId)
			db_conn.execute(statement)
			db_conn.commit()
	except Exception:
		return False
	return True



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
