class User:
    id = None
    fname = None
    lname = None
    age = None
    sex = None
    weight = None
    maintenance = None
    has_workout = True
    #UPDATE THIS HSIT

    def __init__(self,attrs):
        self.id = attrs[0]
        self.fname = attrs[1]
        self.lname = attrs[2]
        self.age = attrs[3]
        self.sex = attrs[4]
        self.weight = attrs[5]
        self.maintenance = attrs[6]