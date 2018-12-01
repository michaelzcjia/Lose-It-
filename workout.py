import numpy as np
import app

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
    workout["weeks"] = None
    workout["mnt"] = None
    workout["dfc"] = None

    def __init__(self, attr):
        '''Get an existing workout'''
        self.workout["id"] = attr[0]
        self.workout["a_id"] = attr[1]
        for i, ex in enumerate(["ex1", "ex2", "ex3", "ex4", "ex5", "ex6"]):
            self.workout[ex] = {"ex":attr[2+(4*i)],"dur":attr[3+(4*i)],"int":attr[4+(4*i)],"rep":attr[5+(4*i)]}
        self.workout["days"] = attr[26]
        self.workout["weeks"] = attr[27]
        self.workout["mnt"] = attr[28]
        self.workout["dfc"] = attr[29]

    def __init__(self, a_id):
        '''Get an existing workout'''
        self.workout["id"] = int(np.random.random()*10000)
        self.workout["a_id"] = a_id

    def generate_workout(self, pref, user, e_df):
        #Get weekly calories needed
        weekly_burn = self.calc_cal(pref,user)

        #How many exercises?
            #Four Exercises (including the two they like, discluding the two they don't)
        #How long is each workout?
            #Check the intensity and pick an "intensity" (from exercises) range based on it
        #Apply filters to exercisees, randomly select 4 of them
        #Make the amount of time each exercise is performed for inversely proportional to the met
        #Each exercise burns the exact same amount of calories, calc the times.
        self.workout["days"] = pref["days"]

        #Per workout burn
        ea_workout_burn = weekly_burn/pref["days"]
        return

    def calc_cal(self, pref, user):
        "Returns the daily caloric burn"
        #Note: make sure to do type conversion (string -> float)
        w = user.weight
        h = user.height
        a = user.age
        s = user.sex
        m_cal = self.calc_maint(w,h,a,s)

        #how many pounds per week do they want to lose?
        lb_per_week = pref.lb_wk
        wkly_def = 0
        if lb_per_week == 1:
            wkly_def = 3500
        if lb_per_week == 1.5:
            wkly_def = 5200
        if lb_per_week == 2:
            wkly_def = 7000

        #how willing they are to diet
        nutr = pref.pref["nutri"]
        if nutr == 1:
            nutr_def = 0
        if nutr == 2:
            nutr_def = wkly_def * 0.3
        if nutr == 3:
            nutr_def = wkly_def * 0.6

        #Required total deficit
        daily_intake = m_cal - nutr_def/7.0

        #Required calories to burn to work from exercise
        wkly_ex_burn_req = wkly_def - nutr_def

        #Weeks needed
        wks_needed = np.ceil((pref.goalw - user.weight)/lb_per_week)

        #Set some fields
        self.workout["weeks"] = wks_needed
        self.workout["dfc"] = daily_intake

        return wkly_ex_burn_req

    def calc_maint(self, weight, height, age, sex):
        '''Calculate maintenance calories'''
        kg_to_lb = 2.20462
        if sex == "M":
            activity_f = 1.2
            const_f = 5
        if sex == "F":
            activity_f = 1.1
            const_f = -161
        cal = height * 6.25 + weight * kg_to_lb * 9.99 - age * 4.92 + const_f
        cal *= activity_f
        return cal




#Create an empty workout object
#Then call create workout
#Get preferences of teh current user
#Get the caloric information of the current user
#Calculate caloric deficit needs
#Pull whole exercise database
#Do filters
#Calculate calories

if __name__ == '__main__':
    #app.run(debug=True, use_reloader=True)
    app.generateWorkout()