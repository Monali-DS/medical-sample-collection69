# -*- coding: utf-8 -*-
"""
Created on Wed May 18 08:09:22 2022
by Monali
"""

# flask app
# importing libraries
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from markupsafe import escape

# flask app
app = Flask(__name__)
df_sample = pd.read_excel("./Cleaned_sample.xlsx")
# df_sample.info()
# loading model
# model_pipe_dt = pickle.load(open('model.pkl', 'rb'))
dt_model = pickle.load(open('./dt_model.pkl', 'rb'))

# df = pd.read_csv('./Cleaned_data.csv')
# rf_model = pickle.load(open('./rf_cl_model.pkl', 'rb'))

@app.route('/')
def index():
    test_name = sorted(df_sample['Test_Name'].unique())
    sample = sorted(df_sample['Sample'].unique())
    # way_of_storage = sorted(df_sample['Way_Of_Storage_Of_Sample'].unique())
    # way_of_storage name dont need to be here used radio buttons insted
    schedule = sorted(df_sample['Cut_off_Schedule'].unique())
    traffic = sorted(df_sample['Traffic_Conditions'].unique())
    
    # test_name.insert(0,"Select Test Name")
    # sample.insert(0,"Select Sample Type")
    # way_of_storage.insert(0,"Select Way of Sample Storage")
    # schedule.insert(0,"Select Cut-off Schedule")
    # traffic.insert(0,"Select Traffic Conditions")
    
    return render_template('index.html', test_name= test_name, sample= sample, 
                            # way_of_storage= way_of_storage, 
                            schedule= schedule, traffic= traffic)

# def home():
#     return render_template('index.html')

@app.route('/prediction' ,methods = ["GET", "POST"])
def prediction():
    test_name = request.form.get('testname')
    # print('test_name:', test_name)
    sample = request.form.get('samplename')
    # print('sample:', sample)
    way_of_storage = request.form.get('newradio')
    test_booking_time = request.form.get('test_booking_time_hh_mm')
    scheduled_sample_collection = request.form.get('scheduled_sample_collection_time_hh_mm')
    cut_off_schedule = request.form.get('schedule')
    cut_off_time = request.form.get('cut_off_time_hh_mm')
    # Agent_ID = int(request.form.get('Agent_ID'))
    traffic_conditions = request.form.get('traffic')
    agents_location = request.form.get('agent_location_km')
    time_taken_to_reach_patient_mm = request.form.get('time_taken_to_reach_patient_mm')
    time_for_sample_collection_mm = request.form.get('time_for_sample_collection_mm')
    lab_location = request.form.get('lab_location_km')
    time_taken_to_reach_lab_mm = request.form.get('time_taken_to_reach_lab_mm')

    data = {
        'Test_Name': test_name,
        'Sample': sample,
        'Way_Of_Storage_Of_Sample': way_of_storage,
        'Test_Booking_Time_HH_MM' : test_booking_time,
        'Scheduled_Sample_Collection_Time_HH_MM' : scheduled_sample_collection,
        'Cut_off_Schedule': cut_off_schedule,
        'Cut_off_time_HH_MM': cut_off_time,
        'Traffic_Conditions': traffic_conditions,
        'Agent_Location_KM': agents_location,
        'Time_Taken_To_Reach_Patient_MM' : time_taken_to_reach_patient_mm,
        'Time_For_Sample_Collection_MM': time_for_sample_collection_mm,
        'Lab_Location_KM': lab_location,
        'Time_Taken_To_Reach_Lab_MM': time_taken_to_reach_lab_mm
        }
    
    print('data:' , data)
    features = pd.DataFrame(data, index=[0])
    print('Features:' , features)
    
    # final_features = [np.array(features)]
    # print('Final Features:' , final_features)
    print('predictiND MODEL')
    prediction = dt_model.predict(features)
    print('prediction:' , prediction)
    
    # final_features = [float(x) for x in request.form.values()]
    # final_features = [np.array(final_features)]
    # prediction = dt_model.predict(final_features)
    
    if prediction == 'Y':
        return render_template("predict.html", output='YES')
       # prediction = 'YES'
       # return render_template('predict.html', output='Will sample reach on or before time? : {}'.format(prediction))
    else:
        return render_template("predict.html", output='NO')
       # prediction = 'NO'
       # return render_template('predict.html', output='Will sample reach on or before time? : {}'.format(prediction))

if __name__ == "__main__":
    app.run(debug=True)