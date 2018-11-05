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
	results = ""
	results = db_conn.execute("SELECT Username FROM Account WHERE Username = '{}' AND Password = '{}'".format(user,password))
	flag = False

	# if results not empty:
	if len(results) > 0:
		flag = True
	# try:
	# 	print("trying")
	# 	for i in result
	# 	print("Triedit")
	# 	flag = True
	# except Exception:
	# 	flag = False
	# 	print("big oops")
	return flag

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

