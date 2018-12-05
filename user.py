import loseit_db

class User:
    id = None
    fname = None
    lname = None
    age = None
    sex = None
    weight = None
    height = None
    maintenance = None

    # UPDATE THIS HSIT

    def __init__(self, attrs):
        self.id = attrs[0]
        self.fname = attrs[1]
        self.lname = attrs[2]
        self.age = attrs[3]
        self.sex = attrs[4]
        self.weight = attrs[5]
        self.height = attrs[6]
        self.maintenance = attrs[7]

    def has_workout(self, db_conn):
        '''Returns True if the user has a workout already'''
        if loseit_db.check_workout(db_conn, self.id):
            return True
        else:
            return False
