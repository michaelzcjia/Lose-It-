import numpy as np
import app
import pandas as pd

class Workout:
    workout = dict()
    workout["id"] = None
    workout["a_id"] = None
    workout["ex1"] = None
    workout["ex2"] = None
    workout["ex3"] = None
    workout["ex4"] = None
    workout["days"] = None
    workout["weeks"] = None
    workout["mnt"] = None
    workout["dfc"] = None

    def __init__(self, attr):
        '''Get an existing workout'''
        self.workout["id"] = attr[0]
        self.workout["a_id"] = attr[1]
        for i, ex in enumerate(["ex1", "ex2", "ex3", "ex4"]):
            self.workout[ex] = {"ex":attr[2+i+(4*i)],"dur":attr[3+i+(4*i)],"int":attr[4+i+(4*i)],"descr":attr[5+i+(4*i)], "img":attr[6+i+(4*i)]}
        self.workout["days"] = attr[22]
        self.workout["weeks"] = attr[23]
        self.workout["mnt"] = attr[24]
        self.workout["dfc"] = attr[25]

    def __init__(self, a_id):
        '''Get an existing workout'''
        self.workout["id"] = int(np.random.random()*10000)
        self.workout["a_id"] = a_id
        for i, ex in enumerate(["ex1", "ex2", "ex3", "ex4", "ex5"]):
            self.workout[ex] = {"ex":None,"dur":None,"int":None,"descr":None, "img":None}

    def generate_workout(self, pref, user, e_data):
        pdic = pref.pref

        #Get weekly calories needed
        weekly_burn = self.calc_cal(pref,user)

        #Select the exercises that the person likes
        e_df = pd.DataFrame(e_data)
        e_df.columns = ["ID","Name","Description","MET","Duration","Intensity","Link"]
        e_df.MET = pd.to_numeric(e_df.MET)
        e_df.Intensity = pd.to_numeric(e_df.Intensity)

        #Delete the exercises to avoid
        e_df = e_df[~e_df['Name'].isin([pdic['a1'],pdic['a2']])]
        #Filter based on intensity
        e_df = e_df[e_df['Intensity'] <= float(pdic['intensity'])]
        #Now random sample until we're good!!!!

        exercises = []
        num_ex = 0

        #Get df with only preferred ones (one a time)
        #Sort in order of intensity, then add the first one

        p1_df = e_df[e_df.Name == pdic['p1']]
        p1_df.sort_values(by = "MET", ascending = False, inplace = True)
        p2_df = e_df[e_df.Name == pdic['p2']]
        p2_df.sort_values(by = "MET", ascending = False, inplace = True)

        #Add the preferred exercises, maximize the intensity
        p1 = p1_df.head(1)
        if not p1.empty:
            exercises.append(p1)
            num_ex += 1
        p2 = p2_df.head(1)
        if not p2.empty:
            exercises.append(p2)
            num_ex += 1

        #Add the rest of them
        while num_ex < 4:
            sample = e_df.sample()
            # print(sample)
            # print("@@@",exercises)
            add = True
            for df in exercises:
                if df.Name.iloc[0] == sample.Name.iloc[0]:
                    add = False
            if add:
                exercises.append(sample)
                num_ex += 1

        #print(exercises)

        self.workout["days"] = pdic["days"]

        # Per workout burn
        ea_workout_burn = weekly_burn / float(pdic["days"])

        # Per exercise burn
        ex_burn = ea_workout_burn / 4.0

        print(ea_workout_burn)
        print(ex_burn)
        #For each exercises, do math and assign it the workout dictionary

        exs = ["ex1", "ex2", "ex3", "ex4"]
        for i, ex in enumerate(exercises):
            #Add exercise name
            self.workout[exs[i]]['ex'] = ex.Name.iloc[0]
            #Add exercise duration
            print(ex_burn,ex.MET.iloc[0],user.weight)
            self.workout[exs[i]]['dur'] = int(60*(ex_burn / (ex.MET.iloc[0] * float(user.weight) * 0.453592 * 4)))
            #Add exercise description
            self.workout[exs[i]]['descr'] = ex.Description.iloc[0]
            #Add exercise
            self.workout[exs[i]]['img'] = ex.Link.iloc[0]
            #Add intensity (even though we don't use it)
            self.workout[exs[i]]['int'] = ex.Intensity.iloc[0]

        #print(self.workout)
        return self.workout

    def calc_cal(self, pref, user):
        "Returns the daily caloric burn"
        #Note: make sure to do type conversion (string -> float)
        w = float(user.weight)
        h = float(user.height)
        a = int(user.age)
        s = user.sex
        m_cal = self.calc_maint(w,h,a,s)

        print(m_cal)

        #how many pounds per week do they want to lose?
        lb_per_week = pref.pref['lb_wk']
        print(lb_per_week)
        wkly_def = 0
        if lb_per_week == "1.0":
            wkly_def = 3500
        if lb_per_week == "1.5":
            wkly_def = 5200
        if lb_per_week == "2.0":
            wkly_def = 7000

        #how willing they are to diet
        nutr = pref.pref["nutri"]
        if nutr == "1":
            nutr_def = 0
        if nutr == "2":
            nutr_def = wkly_def * 0.3
        if nutr == "3":
            nutr_def = wkly_def * 0.6

        #Required total deficit
        daily_intake = m_cal - nutr_def/7.0

        #Required calories to burn to work from exercise
        wkly_ex_burn_req = wkly_def - nutr_def

        print(lb_per_week,pref.pref['goalw'])

        #Weeks needed
        wks_needed = np.ceil((w - float(pref.pref['goalw']))/float(lb_per_week))

        #Set some fields
        self.workout["weeks"] = int(wks_needed)
        self.workout["dfc"] = int(daily_intake)
        self.workout['mnt'] = int(m_cal)

        print(wks_needed,daily_intake,m_cal)

        return wkly_ex_burn_req

    def calc_maint(self, weight, height, age, sex):
        '''Calculate maintenance calories'''
        kg_to_lb = 2.20462
        print(sex)
        if sex == "M":
            activity_f = 1.2
            const_f = 5
        if sex == "F":
            activity_f = 1.1
            const_f = -161
        cal = height * 6.25 + weight / kg_to_lb * 9.99 - age * 4.92 + const_f
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