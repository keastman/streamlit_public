import numpy as np

def speed_to_pace(mph):
    '''converts an mph to a pace string min:mi'''
    pace_min_mi = 60/mph
    hours = np.floor(pace_min_mi/60)
    mins = pace_min_mi - hours*60
    out = "%2d:%02d" % (np.floor(mins), 60*(pace_min_mi-np.floor(pace_min_mi)))
    if hours > 0:
        out = "%02d:%02d" % (np.floor(mins), 60*(pace_min_mi-np.floor(pace_min_mi)))
        out = '%d:' %(hours)+out
    return out

def race_predict(z_mph):
    '''converts zone speeds to race predictions '''
    race_mph = [
        z_mph[3], # 1-mile
        (z_mph[3]*0.8 + 0.2*z_mph[2]), # 2-mile
        (z_mph[3]+z_mph[2])/2, #5k
        z_mph[2], #10k
        (z_mph[1]+z_mph[2])/2, #half-marathon
        z_mph[1] # marathon
        ]
    return race_mph

def get_zones(lt,vo2max,re):
    ''' 
    inputs - core metics (lt,vo2max,re)
    returns - arrays for (lt1,mgp,lt2,vo2max,sprint)
        z_pct - lt1_mgp_lt2_spt_pct
        z_mph = speeds (y axis)
        z_vo2 = vo2s (x axis)
    '''
    z_pct = np.array(
        [100-2*(100-lt),
         100-1.5*(100-lt),
         lt,
         100,
         100+0.5*(100-lt)]
        )/100.0 

    z_mph = z_pct*0.624*60*vo2max/re
    z_vo2 = z_pct*vo2max
    return z_pct,z_mph,z_vo2