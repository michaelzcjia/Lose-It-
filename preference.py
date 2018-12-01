class Preference:
    pref = dict()
    pref["a_id"] = None
    pref["p1"] = None
    pref["p2"] = None
    pref["a1"] = None
    pref["a2"] = None
    pref["lb_wk"] = None
    pref["days"] = None
    pref["intensity"] = None
    pref["nutri"] = None
    pref["goalw"] = None

    def __init__(self, attr):
        self.pref["a_id"] = attr[0]
        self.pref["p1"] = attr[1]
        self.pref["p2"] = attr[2]
        self.pref["a1"] = attr[3]
        self.pref["a2"] = attr[4]
        self.pref["weeks"] = attr[5]
        self.pref["days"] = attr[6]
        self.pref["intensity"] = attr[7]
        self.pref["nutri"] = attr[8]
        self.pref["goalw"] = attr[9]




