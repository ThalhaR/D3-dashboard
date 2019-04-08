from flask_restful import Resource
from flask_pymongo import PyMongo
from flask import current_app, request
from bson.json_util import dumps , loads
import pandas as pd 
from pandas.io.json import json_normalize
import numpy as np 
import statistics
import datetime
import json
import calendar


def enddate():
    date = request.form.get("month")
    if (date is not None):
        month = '{:%m}'.format(datetime.datetime.strptime(date, '%Y-%m'))
        year ='{:%Y}'.format(datetime.datetime.strptime(date, '%Y-%m'))
        year1 = int(year)
        month1 = int(month)
        day = str(calendar.monthrange(year1,month1 )[1])
        edate = year + "-" + month + "-" + day
    else:
         edate = "0"
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth1 = first - datetime.timedelta(days=1)
    startdate1 = lastMonth1.strftime('%Y-%m-%d')
    if (len(edate) > 8):
        startdate = edate
    else:
        startdate = startdate1
    return startdate

def enddate2():
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth1 = first - datetime.timedelta(days=1)
    startdate = str(lastMonth1)
    startdate = '{:%Y-%m}'.format(datetime.datetime.strptime(startdate, '%Y-%m-%d'))
    return startdate

def enddate3():
    today = datetime.date.today()
    first = today.replace(day=1)
    first = first - datetime.timedelta(days=1)
    startdate = str(first)
    startdate = '{:%Y-%m}'.format(datetime.datetime.strptime(startdate, '%Y-%m-%d'))
    return startdate

def enddate1():
    today = datetime.date.today()
    first = today.replace(day=1)
    first = first - datetime.timedelta(days=1)
    startdate = first.strftime('%Y-%m-%d')
    return startdate

def startdate():
    date = request.form.get("month")
    if (date is not None):
        sdate = date + "-01"
    else:
        sdate = "0"
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth1 = first - datetime.timedelta(days=1)
    startdate3 = lastMonth1.replace(day = 1)
    startdate1 = startdate3.strftime('%Y-%m-%d')
    if (len(sdate) > 8):
        startdate = sdate
    else:
        startdate = startdate1
    
    return startdate

# def startdate2():
#     today = datetime.date.today()
#     first = today.replace(day=1)
#     lastMonth1 = first - datetime.timedelta(days=1)
#     startdate3 = lastMonth1.replace(day = 1)
#     startdate2 = startdate3 - datetime.timedelta(days=1)
#     startdate1 = startdate2.replace(day = 1)
#     startdate1 = startdate1 - datetime.timedelta(days=100)
#     startdate = startdate1.strftime('%Y-%m-%d')
#     return startdate

def startdate1():
    today = datetime.date.today()
    first = today.replace(day=1)
    startdate = first - datetime.timedelta(days=365)
    startdate = startdate.strftime('%Y-%m-%d')
    return startdate


def month_name():
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth1 = first - datetime.timedelta(days=1)
    startdate1 = lastMonth1.replace(day = 1)
    startdate1 = str(startdate1)
    startdate = '{:%B}'.format(datetime.datetime.strptime(startdate1, '%Y-%m-%d'))
    return startdate

# def data_year():
#     mongo = current_app.db
#     data = mongo.db.patients.find({'admission.date_of_admission': {
#                         '$gte': startdate1(),
#                         '$lte': enddate1()}})
    
#     return data

def data5():
    mongo = current_app.db
    data = dumps(mongo.db.patients.find())
    patient = json.loads(data)
    data1 = pd.DataFrame(patient) 
    pd.set_option('display.max_columns', 300)
    data2 = data1['admission'].apply(pd.Series)
    data = data2
    if 'discharge' in patient:
        data3 = data1['discharge'].apply(pd.Series)
        data = data.join(data3)
    if 'admissionAssessment' in patient:
        data4 = data1['admissionAssessment'].apply(pd.Series)
        data = data.join(data4) 
    if 'preQol' in patient:
        if patient['preQol'] > 0 :
            data5 = data1['preQol'].apply(pd.Series)
            data5 = data5[0].apply(pd.Series)
            data = data.join(data5)
    if 'postQol' in patient:
        if patient['postQol'] > 0 :
            data7 = data1['postQol'].apply(pd.Series)
            data8 = data7[0].apply(pd.Series)
            data = data.join(data8,lsuffix = '.pre' , rsuffix='.post')


    
    data6 = [1] * len(data2)
    
    
    
    
    data['num'] = data6
    
    return data

def assessment_data():
    mongo = current_app.db
    data = dumps(mongo.db.patients.find())
    patients = json.loads(data)
    pd.set_option('display.max_columns', 300)
    assessment_list = []
    uni = []

    if 'daily_assessment' in patients :
        for data in patients:
            if len(data['daily_assessment']) >0:
                for asssesment in data['daily_assessment']:
                    unid = data['admission']['patient_id']
                    # unid = data['admission']['patient_id']
                    assessment_list.append(asssesment)
                    uni.append(unid)
        data2 = pd.DataFrame(assessment_list)
        data2['patient_id'] = uni
        data = data2[(data2['date_of_daily_assessment'] >= startdate()) & (data2['date_of_daily_assessment'] <= enddate())]
    else :
        data = "No Data"

    return data

def data1():
    data2 = data5()
    data = data2[(data2['date_of_admission'] >= startdate1()) & (data2['date_of_admission'] <= enddate1())]

    return data

def datas():
    data2 = data5()
    data = data2[(data2['date_of_admission'] >= startdate()) & (data2['date_of_admission'] <= enddate())]
    return data
    
def avg_monthly_admission():
    data = data1()
    patients = len(data)
    avg = patients/12
    avg = round(avg)
    return avg

def admission_month():
    data = datas()
    patients = len(data)
    return patients

def diagnosis():
    data = datas()
    if 'Diagnosis' in data :
        data1 = data.groupby('Diagnosis', as_index=False).agg({"num": "sum"})
        data1 = data1.to_json(orient = "records")
    else:
        data1 = "No data"
    return data1

def diagnosis_type():
    data = datas()
    if 'diagnosis_type' in data :
        non = list(data['diagnosis_type']).count("non_operative")
        post = list(data['diagnosis_type']).count("post_operative")
        all = non + post
        if non != 0 & post != 0 :
            non = non/all * 100
            post = post/all * 100
            non = round(non)
            post = round(post)
            non = non.astype(float)
            post = post.astype(float)
        else:
            non = "No data"
            post = "No data"
    else:
        non = "No data"
        post = "No data"
    return {'non' : non , 'post' : post}

def discharge_status():
    data = data1()
    if 'dateofdischarge' in data.columns :
        data['dateofdischarge'] = pd.to_datetime(data['dateofdischarge'],format='%Y-%m-%d')
        data['dateofdischarge'] = data['dateofdischarge'].dt.strftime('%m/%Y')
        data['dateofdischarge'] = pd.to_datetime(data['dateofdischarge'],
                                format='%m/%Y')
        data2 = data.pivot_table(index='dateofdischarge',columns='discharge_status',aggfunc=sum)
        data2.fillna(0,inplace=True)
        data2.columns = data2.columns.droplevel()
        data2.columns.name = None
        data2 = data2.reset_index().to_json(orient='records', date_format='iso', date_unit='s')
    else: data2 = "No data"
    return data2

def admission_type():
    data = datas()
    planned = list(data['admission_type']).count("Planned")
    un = list(data['admission_type']).count("Unplanned")
    if planned != 0 and un != 0 :
        data1 = planned/un
        data1 = round(data1,1)
    else:
        data1 = "No data"
    return data1

def mechanically_ventilated():
    data = datas()
    if 'mechanically_ventilated' in data :
        yes = list(data['mechanically_ventilated']).count("Yes")
        yes1 = yes.astype(float)
        per = yes/admission_month() * 100
        per = "%.1f" % round(per,1)
    else: 
        yes1 = "No data"
        per = "No data" 
    return {'count' : yes1,'per' : per}

def cardiovascular_support():
    data = datas()
    if 'vasoactive_drugs' in data :
        data1 = data.groupby('vasoactive_drugs', as_index=False).agg({"num": "sum"})
        no = data1['num'].iloc[-1]
        yes = admission_month() - no
        yes1 = yes.astype(float)
        per = yes/admission_month() * 100
        per = "%.1f" % round(per,1)
    else: 
        yes1 = "No data"
        per = "No data" 
    return {'count' : yes1,'per' : per}

def trackeostomy():
    data = assessment_data()
    if 'mechanically_ventilated_source' in data :
        data = data.loc[data['mechanically_ventilated_source'] == 'Tracheostomy']
        trackeostomy = data['patient_id'].nunique().count()
        trackeostomy = trackeostomy.astype(float)
    else :
        trackeostomy = "No data"
    return trackeostomy

# def Number_of_tracheostomy():
#     data = assessment_data()
#     data3 = data.groupby('mechanically_ventilated_source').count()
#     Tracheostomy = data3['patient_id'][2]
#     return Tracheostomy

def use_of_antibiotics():
    data = datas()
    if 'antibiotics' in data:
        yes = list(data['antibiotics']).count("Yes")
        yes1 = yes.astype(float)
        per = yes/admission_month() * 100
        per = "%.1f" % round(per,1)
    else: 
        yes1 = "No data" 
        per = "No data"
    return {'count' : yes1,'per' : per}

def lenght_of_stay():
    data = datas()
    if 'dateofdischarge' in data.columns :
        data['dateofdischarge'] = pd.to_datetime(data['dateofdischarge'],format='%Y-%m-%d')
        data['date_of_admission'] = pd.to_datetime(data['date_of_admission'],format='%Y-%m-%d')
        data['Lenght_of_stay'] = (data['dateofdischarge'] - data['date_of_admission']).dt.days
        lenghts = data['Lenght_of_stay'].mean()
        lenghts = "%.1f" % round(lenghts,1)
    else: lenghts = "No data"

    return lenghts

def mean_days_mechanically_ventilated():
    data = assessment_data()
    if 'mechanically_ventilated' in data :
        days = (list(data['mechanically_ventilated']).count("Yes"))/admission_month()
        days = "%.1f" % round(days,1) 
    else: days = "No data"
    # patents = data['patient_id'].nunique()
    # days = (list(data['mechanically_ventilated']).count("Yes"))/patents
    return days

def time_on_antibiotics():
    data = assessment_data()
    if 'antibiotics' in data :
        days = (list(data['antibiotics']).count("Yes"))/admission_month()
        days = "%.1f" % round(days,1)
    # days = (list(data['antibiotics']).count("Yes"))/patents
    # # patents = data['patient_id'].nunique()
    else: days = 'No data'
    
    return days

def scale(x):
    x = x.replace(['Limited, or did not do for other reasons','Severely Limited','Moderately Limited','Somewhat Limited','A Little Limited','Not Limited'], [1,2,3,4,5,6])
    return x

def saq_score():
    data = datas()
    if 'lifting_or_moving_heavyOb.post' in data :
        data['lifting_or_moving_heavyOb.post'] = scale(data['lifting_or_moving_heavyOb.post'])
        data['dressing_yourself.post'] = scale(data['dressing_yourself.post'])
        data['how_about_your_health_today.post'] = scale(data['how_about_your_health_today.post'])
        data['walking_more_than_Block.post'] = scale(data['walking_more_than_Block.post'])
        data['running_or_jogging.post'] = scale(data['running_or_jogging.post'])
        data['showering.post'] = scale(data['showering.post'])
        data['walking_indoors_on_level_ground.post'] = scale(data['walking_indoors_on_level_ground.post'])
        data['climbing_hill_or_fligh.post'] = scale(data['climbing_hill_or_fligh.post'])
        data['gardening_vacuuming_or_carrying.post'] = scale(data['gardening_vacuuming_or_carrying.post']) 
        data['participating_in_strenuous.post'] = scale(data['participating_in_strenuous.post'])
        data['saq_score'] = (data['lifting_or_moving_heavyOb.post'] + data['dressing_yourself.post'] +  data['how_about_your_health_today.post'] + data['walking_more_than_Block.post'] + data['running_or_jogging.post'] + data['showering.post'] + data['walking_indoors_on_level_ground.post'] +  data['climbing_hill_or_fligh.post'] + data['gardening_vacuuming_or_carrying.post'] + data['participating_in_strenuous.post'])/60 * 100
        mean_saq = data['saq_score'].mean()
        mean_saq = "%.1f" % round(mean_saq,1)
    else :
        mean_saq = "No data"
    return mean_saq

# def eq():
#     data = datas()
#     MO_pre = data["mobility"].replace(['I have no problems in walking about','I have slight problems in walking about','I have moderate problems in walking about','I have severe problems in walking about','I am unable to walk about'],[5,4,3,2,1])
#     SC_pre = data['selfCare'].replace(['I have no problems washing or dressing myself','I have slight problems washing or dressing myself','I have moderate problems washing or dressing myself','I have severe problems washing or dressing myself','I am unable to wash or dress myself'],[5,4,3,2,1])
#     UN_pre = data['usual_activities'].replace(['I have no problems doing my usual activities','I have slight problems doing my usual activities',' I have moderate problems doing my usual activities',' I have severe problems doing my usual activities',' I am unable to do my usual activities'],[5,4,3,2,1])
#     PD_pre = data['pain_discomfort'].replace(['I have no pain or discomfort','I have slight pain or discomfort','I have moderate pain or discomfort','I have severe pain or discomfort','I have extreme pain or discomfort'],[1,2,3,4,5])
#     AD_pre = data['anxiety_depression'].replace(['I am not anxious or depressed','I am slightly anxious or depressed','I am moderately anxious or depressed','I am severely anxious or depressed','I am extremely anxious or depressed'],[1,2,3,4,5])
#     MO_pre = MO_pre.mean()
#     SC_pre = SC_pre.mean()
#     UN_pre = UN_pre.mean()
#     PD_pre = PD_pre.mean()
#     AD_pre = AD_pre.mean()
#     answers = [1,0.879,0.848]
#     MO = 1
#     SC = 1 
#     UN = 1 
#     PD = 1 
#     AD = 1
#     for ans in answers:
#         while AD > 6:
#             SC = 1
#             UN = 1
#             MO = 1 
            # PD = 1
            
def patient_satisfation():
    data = datas()
    if 'overall_satisfaction' in data :
        satisfaction = data['overall_satisfaction'].replace(['Not satisfied at all','Mostly dissatisfied','Somewhat satisfied',"Mostly satisfied",'Highly satisfied'], [1,2,3,4,5])
        mean_satisfaction = satisfaction.mean()/5
        mean_satisfaction = round(mean_satisfaction*5)/5
        if mean_satisfaction == 0.6 :
            x = "Somewhat satisfied"
        elif mean_satisfaction == 0.8:
            x = "Mostly satisfied"
        elif mean_satisfaction == 0.4:
            x = "Mostly dissatisfied"
        elif mean_satisfaction == 1 :
            x = "Highly satisfied"
        elif mean_satisfaction == 0.2 :
            x = "Not satisfied at all"
        else : x = "No data"
    else: x = "No data"
    
    return x

def drill_down_chart():
    data = datas()
    sep = ','
    # data['apache_iv_condition'] = data['apache_iv_condition'].str.split(sep, 1)[0]
    if 'Diagnosis' in data :
        data1 = data.groupby(['Diagnosis', 'apache_iv_condition'], as_index=False).agg({'num': 'sum'})
        data1 = data1.to_json(orient = "records")
    else : data1 = 'No data '

    return data1

def type_of_antibiotic():
    data = datas()
    if 'name_of_the_antibiotic' in data :
        data1 = data.groupby('name_of_the_antibiotic', as_index=False).agg({"num": "sum"})
        data1 = data1.to_json(orient = "records")
    else : data1 = 'No data'
    return data1

def apache_score():
    data = datas()
    if 'APACHE_score' in data :
        data1 = data.loc[data['admission_type'] == 'Unplanned']
        data2 = data.loc[data['admission_type'] == 'Planned']
        p = data1['APACHE_score']
        u = data2['APACHE_score']
        sp = np.std(np.array(list(data2.loc[:,"APACHE_score"]),float))
        su = np.std(np.array(list(data1.loc[:,"APACHE_score"]),float))
        ap = np.mean(np.array(list(data2.loc[:,"APACHE_score"]),float))
        au = np.mean(np.array(list(data1.loc[:,"APACHE_score"]),float))
        sp = round(sp,2)
        su = round(su,2)
        ap = round(ap,2)
        au = round(au,2)
    else :
        ap = 'No data'
        au = 'No data'
        sp = 'No data'
        su = 'No data'

    return {'APACHE_planned': ap,'APACHE_unplanned' : au,'stand_planned' : sp, 'stand_unplanned' : su}




# x = admission_type()
# print(x)

class VizData(Resource):

    def get(self):
         
        return{'APACHE':apache_score() ,'patient_satisfation' : patient_satisfation(),'type_of_antibiotic' : type_of_antibiotic(),'dril': drill_down_chart(),'max' : enddate3() ,'values' : enddate2() ,'date1' : enddate(),'date' : startdate(), 'cardiovascular_support' : cardiovascular_support(),'avg_monthly_admission' : avg_monthly_admission(), 'saq_score' : saq_score() ,'time_on_antibiotics' : time_on_antibiotics(),  'mean_days_mechanically_ventilated' : mean_days_mechanically_ventilated() , 'lenght_of_stay' : lenght_of_stay() , 'use_of_antibiotics' : use_of_antibiotics() , 'trackeostomy' : trackeostomy() , 'mechanically_ventilated' : mechanically_ventilated() , 'discharge_status' : discharge_status() , 'diagnosis_type' : diagnosis_type() , 'diagnosis' : diagnosis() , 'admission_month' : admission_month(), 'month_name' : month_name(), 'admission_type' : admission_type() }

    def post(self):
        return{'APACHE':apache_score() ,'patient_satisfation' : patient_satisfation(),'type_of_antibiotic' : type_of_antibiotic() , 'dril': drill_down_chart(),'max' : enddate3() ,'values' : enddate2() ,'date1' : enddate(),'date' : startdate(), 'cardiovascular_support' : cardiovascular_support(),'avg_monthly_admission' : avg_monthly_admission(), 'saq_score' : saq_score() ,'time_on_antibiotics' : time_on_antibiotics(),  'mean_days_mechanically_ventilated' : mean_days_mechanically_ventilated() , 'lenght_of_stay' : lenght_of_stay() , 'use_of_antibiotics' : use_of_antibiotics() , 'trackeostomy' : trackeostomy() , 'mechanically_ventilated' : mechanically_ventilated() , 'discharge_status' : discharge_status() , 'diagnosis_type' : diagnosis_type() , 'diagnosis' : diagnosis() , 'admission_month' : admission_month(), 'month_name' : month_name(), 'admission_type' : admission_type() }
 