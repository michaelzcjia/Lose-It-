class Workout:
    workout = dict()
    workout["id"] = None
    workout["a_id"] = None
    workout["ex1"] = None
    workout["ex2"] = None
    workout["ex3"] = None
    workout["ex4"] = None
    workout["ex5"] = None
    workout["days"] = None
    workout["months"] = None
    workout["mnt"] = None
    workout["dfc"] = None

    def __init__(self, attr):
        self.workout["id"] = attr[0]
        self.workout["a_id"] = attr[1]
        for i, ex in enumerate(["ex1", "ex2", "ex3", "ex4", "ex5"]):
            self.workout[ex] = {"ex":attr[2+i+(4*i)],"dur":attr[3+i+(4*i)],"int":attr[4+i+(4*i)],"descr":attr[5+i+(4*i)], "img":attr[6+i+(4*i)]}
        self.workout["days"] = attr[27]
        self.workout["months"] = attr[28]
        self.workout["mnt"] = attr[29]
        self.workout["dfc"] = attr[30]
