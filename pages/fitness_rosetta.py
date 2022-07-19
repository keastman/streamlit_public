import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.markdown('''# Fitness Rosetta 🚴🏃''')
st.markdown('''
    interactive comparison of running, cycling, & physiological metrics
    ''')


#### FUNCTIONS
def speed_to_pace(mph):
    pace_min_mi = 60/mph
    hours = np.floor(pace_min_mi/60)
    mins = pace_min_mi - hours*60
    out = "%2d:%02d" % (np.floor(mins), 60*(pace_min_mi-np.floor(pace_min_mi)))
    if hours > 0:
        out = "%02d:%02d" % (np.floor(mins), 60*(pace_min_mi-np.floor(pace_min_mi)))
        out = '%d:' %(hours)+out
    return out

def y_mph_to_race_mph(y):
    '''converts y axis in mph to prs for distances'''
    return [
        y[3], # 1-mile
        (y[3]*0.8 + 0.2*y[2]), # 2-mile
        (y[3]+y[2])/2, #5k
        y[2], #10k
        (y[1]+y[2])/2, #half-marathon
        y[1] # marathon
        ]

def make_race_prediction_df(re,lt,vo2max):
    df = pd.DataFrame(np.random.rand(6,2),index=dist_names, columns=['Time','Pace'])
    return df


# distance dictionary
dist_dict = {'1M':1,
     '2M':2,
     '5k':3.105,
     '10k':6.21,
     '13.1M':13.1,
     '26.2M':26.2}

# pace labels
labels = ['LT1','MGP','LT2','V02MAX','SPRINT']

# x-axis options for graph
x_options = [
    'v02',
    'power',
    'power/weight',
    'energy consumption',
    'METs',
    'v02 estimations']

# plot limits
vo2axes = np.arange(30,81,5) 
pace_axes = np.arange(12, 5.4, -0.5) # pace min/mi
speed_axes = 60/pace_axes
re_axes = np.arange(150,250.01,10)
axcolor = np.array([1,1,1])*0.9

# thresholds
thresh_names = ['MGP','LT','VO2MAX']


#### INITIALIZE COMPONENTS
st.sidebar.markdown('# Metrics')
vo2max = st.sidebar.slider('VO2 (ml/kg/min)', min_value=30, max_value=100, value=50, step=2)
lt = st.sidebar.slider('Lactate Threshold (% of V02max)', min_value=60, max_value=100, value=90, step=2)
re = st.sidebar.slider('RE (ml/kg)', min_value=150, max_value=250, value=220, step=2)
st.sidebar.markdown('### for estimators')
w_kg = st.sidebar.slider('weight (kg)', min_value=40, max_value=120, value=80)
age = st.sidebar.slider('age (yrs)', min_value=10, max_value=70, value=30)
resting_hr = st.sidebar.slider('resting hr (bpm)', min_value=40, max_value=90, value=50)
max_hr = st.sidebar.slider('max hr (bpm)', min_value=140, max_value=220, value=180)


st.sidebar.markdown('## Show:')
graph_checkbox_bool = st.sidebar.checkbox("graph", True, key=1)
if graph_checkbox_bool:
    x_axis_selectbox = st.sidebar.selectbox('X-axis', x_options)
race_prediction_bool = st.sidebar.checkbox("race predictions", False, key=2)
ref_checkbox_bool = st.sidebar.checkbox("references", False, key=4)


#### UPDATE ESTIMATES based on vo2max & LT
lt1_mgp_lt2_spt_pct = np.array(
    [100-2*(100-lt),
     100-1.5*(100-lt),
     lt,
     100,
     100+0.5*(100-lt)]
    )/100.0 
y_mphs= lt1_mgp_lt2_spt_pct*0.624*60*vo2max/re
x_vo2s = lt1_mgp_lt2_spt_pct*vo2max
 

### FUNCTIONALITY 
if graph_checkbox_bool:
    fig, ax = plt.subplots()
    plt.plot(x_vo2s,y_mphs)
    plt.plot(x_vo2s,y_mphs,'.')
    plt.xlabel(x_axis_selectbox)
    plt.ylabel('pace (min/mi)')
    
    lab_list2 = ['','','','','']
    
    # interactive x axis
    for i,h in enumerate(x_vo2s):
        lab_list2[i] = ax.text(x_vo2s[i],y_mphs[i]-0.15, '%s %d' %(labels[i], 100*lt1_mgp_lt2_spt_pct[i]))
    if x_axis_selectbox=='power':
        ax.set_xticks(vo2axes)
        ax.set_xticklabels(['%d \n %2.0f' %(v,(0.22*w_kg*v*5*4184.0)/(1000*60)) for v in vo2axes])
        ax.set_xlabel('V02 (ml/kg/min) \n power (watts)', fontsize=12)
    elif x_axis_selectbox=='power/weight':
        ax.set_xticks(vo2axes)
        ax.set_xticklabels(['%d \n %2.1f' %(v,(0.22*v*5*4184.0)/(1000*60)) for v in vo2axes])
        ax.set_xlabel('V02 (ml/kg/min) \n power/weight (watts/kg)', fontsize=12)
    elif x_axis_selectbox=='energy consumption':
        ax.set_xticks(vo2axes)
        ax.set_xticklabels(['%d \n %2.0f' %(v,(v*w_kg*5*60.0)/(1000)) for v in vo2axes])
        ax.set_xlabel('V02 (ml/kg/min) \n cals/hr', fontsize=12)
    elif x_axis_selectbox=='METs (1.05 Cals/kg/hr)':
        ax.set_xticks(vo2axes)
        ax.set_xticklabels(['%d \n %2.0f' %(v,(v*5*60.0)/(1000*1.05)) for v in vo2axes])
        ax.set_xlabel('V02 (ml/kg/min) \n METs', fontsize=12)
    elif x_axis_selectbox=='v02 estimations':
        ax.axvline(15*max_hr/resting_hr,label= 'Uth et al., 2004',color='r')
        ax.axvline(1000*(3.542+(-0.014*age) + (0.015*w_kg) + (-0.011*resting_hr))/w_kg,label= 'Rexhepi et al., 2014', color='g')
        ax.set_xlabel('V02 (ml/kg/min)', fontsize=12)
        ax.legend()
    elif x_axis_selectbox=='v02':
        ax.set_xticks(vo2axes)
        ax.set_xticklabels(vo2axes)
        ax.set_xlabel('V02 (ml/kg/min)', fontsize=12)
        
    ax.set_yticks(speed_axes)
    ax.set_yticklabels([speed_to_pace(y) for y in speed_axes])
    plt.grid()
    plt.axis([30,80,5,11.5])
    st.pyplot(fig)

    
if race_prediction_bool:
    st.markdown('### Race Predictions')
    race_mph = y_mph_to_race_mph(y_mphs)
    race_pace = [speed_to_pace(y) for y in race_mph]
    t = np.array(race_mph)/np.array(list(dist_dict.values()))
    race_times = [speed_to_pace(y) for y in t]
    df = pd.DataFrame(
            {
             'time': race_times,
             'pace': race_pace
            },
            index=dist_dict.keys())
    st.table(df)



    
if ref_checkbox_bool:
    st.markdown('''
    ## References:
    ### v02max
    BURGER, S.C. et al. (1990) Assessment of the 2.4 km run as a predictor of aerobic capacity. S Afr Med J. 15 (78), p. 327-329.

    UTH, N. et al. (2004) Estimation of VO2 max from the ratio between HRmax and HRrest - the Heart Rate Ratio Method". Eur J Appl Physiol. 91(1), p.111-115

    REXHEPI, A. M. et al. (2014) Prediction of vo2max based on age, body mass, and resting heart rate. Human Movement. 15 (1), p. 56-59.

    DANIELS, J. (2005) Daniels Running Formula. 2nd Ed. Leeds, UK: Human Kinetics. p. 48

    ### Lactate Threshold
    Wearable lactate threshold predicting device is valid and reliable in runners.
    Borges, Nattai R.; Driller, Matthew W.


    J Strength Cond Res. 2005 Aug;19(3):553-8.
    A comparison of methods for estimating the lactate threshold.
    McGehee JC1, Tanner CJ, Houmard JA.


    ### Running Economy
    Mechanisms for Improved Running Economy in Beginner Runners
    ISABEL S. MOORE, ANDREW M. JONES, and SHARON J. DIXON
    Bioenergetics and Human Performance Research Group, Sport and Health Sciences, College of Life and Environmental Sciences, St. Luke’s Campus, University of Exeter, Exeter, UNITED KINGDOM

    de Ruiter, C. J., Verdijk, P. W., Werker, W., Zuidema, M. J., & de Haan, A. (2014). Stride frequency in relation to oxygen consumption in experienced and novice runners. European journal of sport science, 14(3), 251-258.
    ''')

    