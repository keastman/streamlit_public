
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
import fit_utils as fu
import streamlit.components.v1 as components


plt.style.use('classic')
st.markdown("<h1 style='text-align: center; color: black;'>🚴🏃Fitness Rosetta🚴🏃</h1>", unsafe_allow_html=True)
#st.sidebar.markdown(''' ## About''')
st.sidebar.markdown('''
    interactive comparison of running, cycling, & physiological metrics
    ''')


#### Constants
# distance dictionary
dist_dict = {'1M':1,
     '2M':2,
     '5k':3.105,
     '10k':6.21,
     '13.1M':13.1,
     '26.2M':26.2}

# pace labels
labels = ['lt1','mgp','lt2','v02Max','sprint']

# x-axis options for graph
x_options = [
    'v02',
    'power',
    'power/weight',
    'energy use',
    'METs',
    'v02 estimators']

# plot limits
vo2axes = np.arange(30,81,5) 
speed_axes = np.arange(5, 12, 0.5) # pace min/mi


#### Initialize components
# sidebar
st.sidebar.markdown('## Show')
graph_checkbox_bool = st.sidebar.checkbox("graph", True, key=1)
race_prediction_bool = st.sidebar.checkbox("race predictions", False, key=2)
ref_checkbox_bool = st.sidebar.checkbox("references", False, key=4)


col1, col2 = st.columns([1, 3])
with col1:
    st.markdown('#### Metrics')
    vo2max = st.slider('VO2 (ml/kg/min)', min_value=30, max_value=90, value=50, step=2)
    lt = st.slider('Lactate Threshold (% of V02max)', min_value=70, max_value=100, value=90, step=2)
    re = st.slider('RE (ml 02/kg/km)', min_value=150, max_value=250, value=220, step=2)


# update estimates for zones - lt1, marathon goal pace (mgp), lt2, vo2, & sprint
z_pct,z_mph,z_vo2 = fu.get_zones(lt,vo2max,re)

# callbacks
if graph_checkbox_bool:
    col2.markdown('#### Energy vs Speed')
    x_axis_selectbox = col1.selectbox('X-axis', x_options)
    if x_axis_selectbox in ['v02 estimators','power','energy use']:
        weight = col1.slider('weight (kg)', min_value=40, max_value=120, value=80)
        if x_axis_selectbox  == 'v02 estimators':
            age = col1.slider('age (yrs)', min_value=20, max_value=70, value=30)
            resting_hr = col1.slider('resting hr (bpm)', min_value=40, max_value=90, value=50)
            max_hr = col1.slider('max hr (bpm)', min_value=140, max_value=220, value=180)
    
    fig, ax = plt.subplots()
    ax.plot(z_vo2,z_mph)
    ax.plot(z_vo2,z_mph,'.')

    for i in range(5):
        ax.plot([0,z_vo2[i]],[z_mph[i],z_mph[i]],color='lightgrey') # horizontal lines
        ax.text(vo2axes[0]+0.2,  z_mph[i]+0.05, fu.speed_to_pace(z_mph[i]),fontweight='bold')
        ax.plot([z_vo2[i],z_vo2[i]],[0,z_mph[i]],color='lightgrey') # horizontal lines
        ax.text(z_vo2[i],z_mph[i]+0.05, '%s %d' %(labels[i], 100*z_pct[i]),fontweight='bold')
        
        
        if x_axis_selectbox=='v02':
            ax.set_xlabel('V02 (ml/kg/min)', fontsize=12)   
            ax.text(z_vo2[i]+0.2,
                    speed_axes[0]+0.05,
                    '%2.0f' %(z_vo2[i]),fontweight='bold')
        elif x_axis_selectbox=='power':
            if i==0:
                ax.set_xlabel('V02 (ml/kg/min) & power (watts)', fontsize=12)
            ax.text(z_vo2[i]+0.2,
                    speed_axes[0]+0.05,
                    '%2.0f' %((0.22*weight*z_vo2[i]*5*4184.0)/(1000*60)),fontweight='bold')
        elif x_axis_selectbox=='power/weight':
            if i==0:
                ax.set_xlabel('V02 (ml/kg/min) & pw (w/kg)', fontsize=12)
            ax.text(z_vo2[i]+0.2,
                    speed_axes[0]+0.05,
                    '%2.1f' %((0.22*z_vo2[i]*5*4184.0)/(1000*60)),fontweight='bold')           
        elif x_axis_selectbox=='energy use':
            if i==0:
                ax.set_xlabel('V02 (ml/kg/min) & energy (cals/hr)', fontsize=12)
            ax.text(z_vo2[i]+0.2,
                speed_axes[0]+0.05,
                '%2.0f' %((z_vo2[i]*weight*5*60.0)/(1000)) ,fontweight='bold')   
        elif x_axis_selectbox=='v02 estimators':
            if i==0:
                ax.set_xlabel('V02 (ml/kg/min)', fontsize=12)    
                ax.axvline(15*max_hr/resting_hr,label= 'Uth et al., 2004',color='r')
                ax.axvline(1000*(3.542+(-0.014*age) + (0.015*weight) + (-0.011*resting_hr))/weight,
                    label= 'Rexhepi et al., 2014', color='g')
                ax.legend(frameon=False)                
    # elif x_axis_selectbox=='METs (1.05 Cals/kg/hr)':
    #     ax.set_xticklabels(['%d \n %2.0f' %(v,(v*5*60.0)/(1000*1.05)) for v in vo2axes])
    #     ax.set_xlabel('V02 (ml/kg/min) \n METs', fontsize=12)
    ax.set_ylabel('speed (mph)')        

    ax.axis([
            30,
            80,
            5,
            np.max([11.5,z_mph[-1]])
        ])

    fig_html = mpld3.fig_to_html(fig)
    with col2:
        components.html(fig_html, height=600)

if race_prediction_bool:
    col2.markdown('### Race Predictions')
    race_mph = fu.race_predict(z_mph)
    race_pace = [fu.speed_to_pace(y) for y in race_mph]
    t = np.array(race_mph)/np.array(list(dist_dict.values()))
    race_times = [fu.speed_to_pace(y) for y in t]
    df = pd.DataFrame(
            {
             'time': race_times,
             'pace': race_pace
            },
            index=dist_dict.keys())
    col2.table(df)

    
    

if ref_checkbox_bool:
    col2.markdown('''
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

    