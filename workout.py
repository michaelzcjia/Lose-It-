class Workout:
    workout = dict()
    workout["id"] = None
    workout["a_id"] = None
    workout["ex1"] = None
    workout["ex2"] = None
    workout["ex3"] = None
    workout["ex4"] = None
    workout["ex5"] = None
    workout["ex6"] = None
    workout["days"] = None
    workout["months"] = None
    workout["mnt"] = None
    workout["dfc"] = None

    def __init__(self, attr):
        self.workout["id"] = attr[0]
        self.workout["a_id"] = attr[1]
        for i, ex in enumerate(["ex1", "ex2", "ex3", "ex4", "ex5", "ex6"]):
            self.workout[ex] = {"ex":attr[2+(4*i)],"dur":attr[3+(4*i)],"int":attr[4+(4*i)],"rep":attr[4+(4*i)]}
        self.workout["days"] = attr[26]
        self.workout["months"] = attr[27]
        self.workout["mnt"] = attr[28]
        self.workout["dfc"] = attr[29]

