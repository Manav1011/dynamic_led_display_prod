from serial_comm.models import SerialCommunication,States,StatesWeekly
from datetime import date,timedelta,datetime
import pandas as pd
from scipy.stats import circmean

# Function will be running every day and insert new averages per day
def fill_daily_states():
    today = date.today()    
    objs = list(SerialCommunication.objects.filter(RTC__date = today).values())
    if(not objs):        
        return
    df = pd.DataFrame(objs).apply(pd.to_numeric,errors='coerce', downcast='float').round(3)

    # For WSPD we'll find arithmetic mean
    WSPD_DF = df['WSPD'].describe()
    WSPD_COUNT= WSPD_DF['count']
    WSPD_MEAN = WSPD_DF['mean']
    WSPD_MIN= WSPD_DF['min']
    WSPD_MAX= WSPD_DF['max']
    WSPD_STD= WSPD_DF['std']
    WSPD_OBJ = States(param='WSPD',count=WSPD_COUNT,mean=WSPD_MEAN,min=WSPD_MIN,max=WSPD_MAX,std=WSPD_STD,date=today)
    WSPD_OBJ.save()
        

    # For WDIR we'll find circular mean
    WDIR_DF = df['WDIR'].describe()
    WDIR_COUNT= WDIR_DF['count']
    WDIR_MEAN = round(circmean(df['WDIR'], high=360, low=0),3)
    WDIR_MIN= WDIR_DF['min']
    WDIR_MAX= WDIR_DF['max']
    WDIR_STD= WDIR_DF['std']
    WDIR_OBJ = States(param='WDIR',count=WDIR_COUNT,mean=WDIR_MEAN,min=WDIR_MIN,max=WDIR_MAX,std=WDIR_STD,date=today)
    WDIR_OBJ.save()

    #FOR ATMP we'll find arithmatic mean
    ATMP_DF = df['ATMP'].describe()
    ATMP_COUNT= ATMP_DF['count']
    ATMP_MEAN = ATMP_DF['mean']
    ATMP_MIN= ATMP_DF['min']
    ATMP_MAX= ATMP_DF['max']
    ATMP_STD= ATMP_DF['std']
    ATMP_OBJ = States(param='ATMP',count=ATMP_COUNT,mean=ATMP_MEAN,min=ATMP_MIN,max=ATMP_MAX,std=ATMP_STD,date=today)
    ATMP_OBJ.save()

    # for humd we'll find arithmetic mean
    HUMD_DF = df['HUMD'].describe()
    HUMD_COUNT= HUMD_DF['count']
    HUMD_MEAN = HUMD_DF['mean']
    HUMD_MIN= HUMD_DF['min']
    HUMD_MAX= HUMD_DF['max']
    HUMD_STD= HUMD_DF['std']
    HUMD_OBJ = States(param='HUMD',count=HUMD_COUNT,mean=HUMD_MEAN,min=HUMD_MIN,max=HUMD_MAX,std=HUMD_STD,date=today)
    HUMD_OBJ.save()

    # For RAIN we'll find arithmetic mean for now
    RAIN_DF = df['RAIN'].describe()
    RAIN_COUNT= RAIN_DF['count']
    RAIN_MEAN = df['RAIN'].sum()
    RAIN_MIN= RAIN_DF['min']
    RAIN_MAX= RAIN_DF['max']
    RAIN_STD= RAIN_DF['std']
    RAIN_OBJ = States(param='RAIN',count=RAIN_COUNT,mean=RAIN_MEAN,min=RAIN_MIN,max=RAIN_MAX,std=RAIN_STD,date=today)
    RAIN_OBJ.save()

    # For SRAD we'll find arithmetic mean
    SRAD_DF = df['SRAD'].describe()
    SRAD_COUNT= SRAD_DF['count']
    SRAD_MEAN = SRAD_DF['mean']
    SRAD_MIN= SRAD_DF['min']
    SRAD_MAX= SRAD_DF['max']
    SRAD_STD= SRAD_DF['std']
    SRAD_OBJ = States(param='SRAD',count=SRAD_COUNT,mean=SRAD_MEAN,min=SRAD_MIN,max=SRAD_MAX,std=SRAD_STD,date=today)
    SRAD_OBJ.save()

    # For BPRS we'll find arithmetic mean
    BPRS_DF = df['BPRS'].describe()
    BPRS_COUNT= BPRS_DF['count']
    BPRS_MEAN = BPRS_DF['mean']
    BPRS_MIN= BPRS_DF['min']
    BPRS_MAX= BPRS_DF['max']
    BPRS_STD= BPRS_DF['std']
    BPRS_OBJ = States(param='BPRS',count=BPRS_COUNT,mean=BPRS_MEAN,min=BPRS_MIN,max=BPRS_MAX,std=BPRS_STD,date=today)
    BPRS_OBJ.save()

    # For WDCH we'll find arithmetic mean
    WDCH_DF = df['WDCH'].describe()
    WDCH_COUNT= WDCH_DF['count']
    WDCH_MEAN = WDCH_DF['mean']
    WDCH_MIN= WDCH_DF['min']
    WDCH_MAX= WDCH_DF['max']
    WDCH_STD= WDCH_DF['std']
    WDCH_OBJ = States(param='WDCH',count=WDCH_COUNT,mean=WDCH_MEAN,min=WDCH_MIN,max=WDCH_MAX,std=WDCH_STD,date=today)
    WDCH_OBJ.save()

    # For DWPT we'll find arithmetic mean
    DWPT_DF = df['DWPT'].describe()
    DWPT_COUNT= DWPT_DF['count']
    DWPT_MEAN = DWPT_DF['mean']
    DWPT_MIN= DWPT_DF['min']
    DWPT_MAX= DWPT_DF['max']
    DWPT_STD= DWPT_DF['std']
    DWPT_OBJ = States(param='DWPT',count=DWPT_COUNT,mean=DWPT_MEAN,min=DWPT_MIN,max=DWPT_MAX,std=DWPT_STD,date=today)
    DWPT_OBJ.save()

    # For P12 we'll find arithmetic mean
    P12_DF = df['P12'].describe()
    P12_COUNT= P12_DF['count']
    P12_MEAN = P12_DF['mean']
    P12_MIN= P12_DF['min']
    P12_MAX= P12_DF['max']
    P12_STD= P12_DF['std']
    P12_OBJ = States(param='P12',count=P12_COUNT,mean=P12_MEAN,min=P12_MIN,max=P12_MAX,std=P12_STD,date=today)
    P12_OBJ.save()

    # For P13 we'll find arithmetic mean
    P13_DF = df['P13'].describe()
    P13_COUNT= P13_DF['count']
    P13_MEAN = P13_DF['mean']
    P13_MIN= P13_DF['min']
    P13_MAX= P13_DF['max']
    P13_STD= P13_DF['std']
    P13_OBJ = States(param='P13',count=P13_COUNT,mean=P13_MEAN,min=P13_MIN,max=P13_MAX,std=P13_STD,date=today)
    P13_OBJ.save()
    
    # For P14 we'll find arithmetic mean
    P14_DF = df['P14'].describe()
    P14_COUNT= P14_DF['count']
    P14_MEAN = P14_DF['mean']
    P14_MIN= P14_DF['min']
    P14_MAX= P14_DF['max']
    P14_STD= P14_DF['std']
    P14_OBJ = States(param='P14',count=P14_COUNT,mean=P14_MEAN,min=P14_MIN,max=P14_MAX,std=P14_STD,date=today)
    P14_OBJ.save()

    # For P15 we'll find arithmetic mean
    P15_DF = df['P15'].describe()
    P15_COUNT= P15_DF['count']
    P15_MEAN = P15_DF['mean']
    P15_MIN= P15_DF['min']
    P15_MAX= P15_DF['max']
    P15_STD= P15_DF['std']
    P15_OBJ = States(param='P15',count=P15_COUNT,mean=P15_MEAN,min=P15_MIN,max=P15_MAX,std=P15_STD,date=today)
    P15_OBJ.save()

    # For P16 we'll find arithmetic mean
    P16_DF = df['P16'].describe()
    P16_COUNT= P16_DF['count']
    P16_MEAN = P16_DF['mean']
    P16_MIN= P16_DF['min']
    P16_MAX= P16_DF['max']
    P16_STD= P16_DF['std']
    P16_OBJ = States(param='P16',count=P16_COUNT,mean=P16_MEAN,min=P16_MIN,max=P16_MAX,std=P16_STD,date=today)
    P16_OBJ.save()

def fill_weekly_states():
    today = date.today()
    one_week_ago = datetime.now() - timedelta(weeks=1)
    objs = list(SerialCommunication.objects.filter(RTC__gte=one_week_ago).values())
    if(not objs):        
        return
    df = pd.DataFrame(objs).apply(pd.to_numeric,errors='coerce', downcast='float').round(3)

    # For WSPD we'll find arithmetic mean
    WSPD_DF = df['WSPD'].describe()
    WSPD_COUNT= WSPD_DF['count']
    WSPD_MEAN = WSPD_DF['mean']
    WSPD_MIN= WSPD_DF['min']
    WSPD_MAX= WSPD_DF['max']
    WSPD_STD= WSPD_DF['std']
    WSPD_OBJ = StatesWeekly(param='WSPD',count=WSPD_COUNT,mean=WSPD_MEAN,min=WSPD_MIN,max=WSPD_MAX,std=WSPD_STD,date=today)
    WSPD_OBJ.save()
        

    # For WDIR we'll find circular mean
    WDIR_DF = df['WDIR'].describe()
    WDIR_COUNT= WDIR_DF['count']
    WDIR_MEAN = round(circmean(df['WDIR'], high=360, low=0),3)
    WDIR_MIN= WDIR_DF['min']
    WDIR_MAX= WDIR_DF['max']
    WDIR_STD= WDIR_DF['std']
    WDIR_OBJ = StatesWeekly(param='WDIR',count=WDIR_COUNT,mean=WDIR_MEAN,min=WDIR_MIN,max=WDIR_MAX,std=WDIR_STD,date=today)
    WDIR_OBJ.save()

    #FOR ATMP we'll find arithmatic mean
    ATMP_DF = df['ATMP'].describe()
    ATMP_COUNT= ATMP_DF['count']
    ATMP_MEAN = ATMP_DF['mean']
    ATMP_MIN= ATMP_DF['min']
    ATMP_MAX= ATMP_DF['max']
    ATMP_STD= ATMP_DF['std']
    ATMP_OBJ = StatesWeekly(param='ATMP',count=ATMP_COUNT,mean=ATMP_MEAN,min=ATMP_MIN,max=ATMP_MAX,std=ATMP_STD,date=today)
    ATMP_OBJ.save()

    # for humd we'll find arithmetic mean
    HUMD_DF = df['HUMD'].describe()
    HUMD_COUNT= HUMD_DF['count']
    HUMD_MEAN = HUMD_DF['mean']
    HUMD_MIN= HUMD_DF['min']
    HUMD_MAX= HUMD_DF['max']
    HUMD_STD= HUMD_DF['std']
    HUMD_OBJ = StatesWeekly(param='HUMD',count=HUMD_COUNT,mean=HUMD_MEAN,min=HUMD_MIN,max=HUMD_MAX,std=HUMD_STD,date=today)
    HUMD_OBJ.save()

    # For RAIN we'll find arithmetic mean for now
    RAIN_DF = df['RAIN'].describe()
    RAIN_COUNT= RAIN_DF['count']
    RAIN_MEAN = RAIN_DF['mean']
    RAIN_MIN= RAIN_DF['min']
    RAIN_MAX= RAIN_DF['max']
    RAIN_STD= RAIN_DF['std']
    RAIN_OBJ = StatesWeekly(param='RAIN',count=RAIN_COUNT,mean=RAIN_MEAN,min=RAIN_MIN,max=RAIN_MAX,std=RAIN_STD,date=today)
    RAIN_OBJ.save()

    # For SRAD we'll find arithmetic mean
    SRAD_DF = df['SRAD'].describe()
    SRAD_COUNT= SRAD_DF['count']
    SRAD_MEAN = SRAD_DF['mean']
    SRAD_MIN= SRAD_DF['min']
    SRAD_MAX= SRAD_DF['max']
    SRAD_STD= SRAD_DF['std']
    SRAD_OBJ = StatesWeekly(param='SRAD',count=SRAD_COUNT,mean=SRAD_MEAN,min=SRAD_MIN,max=SRAD_MAX,std=SRAD_STD,date=today)
    SRAD_OBJ.save()

    # For BPRS we'll find arithmetic mean
    BPRS_DF = df['BPRS'].describe()
    BPRS_COUNT= BPRS_DF['count']
    BPRS_MEAN = BPRS_DF['mean']
    BPRS_MIN= BPRS_DF['min']
    BPRS_MAX= BPRS_DF['max']
    BPRS_STD= BPRS_DF['std']
    BPRS_OBJ = StatesWeekly(param='BPRS',count=BPRS_COUNT,mean=BPRS_MEAN,min=BPRS_MIN,max=BPRS_MAX,std=BPRS_STD,date=today)
    BPRS_OBJ.save()

    # For WDCH we'll find arithmetic mean
    WDCH_DF = df['WDCH'].describe()
    WDCH_COUNT= WDCH_DF['count']
    WDCH_MEAN = WDCH_DF['mean']
    WDCH_MIN= WDCH_DF['min']
    WDCH_MAX= WDCH_DF['max']
    WDCH_STD= WDCH_DF['std']
    WDCH_OBJ = StatesWeekly(param='WDCH',count=WDCH_COUNT,mean=WDCH_MEAN,min=WDCH_MIN,max=WDCH_MAX,std=WDCH_STD,date=today)
    WDCH_OBJ.save()

    # For DWPT we'll find arithmetic mean
    DWPT_DF = df['DWPT'].describe()
    DWPT_COUNT= DWPT_DF['count']
    DWPT_MEAN = DWPT_DF['mean']
    DWPT_MIN= DWPT_DF['min']
    DWPT_MAX= DWPT_DF['max']
    DWPT_STD= DWPT_DF['std']
    DWPT_OBJ = StatesWeekly(param='DWPT',count=DWPT_COUNT,mean=DWPT_MEAN,min=DWPT_MIN,max=DWPT_MAX,std=DWPT_STD,date=today)
    DWPT_OBJ.save()

    # For P12 we'll find arithmetic mean
    P12_DF = df['P12'].describe()
    P12_COUNT= P12_DF['count']
    P12_MEAN = P12_DF['mean']
    P12_MIN= P12_DF['min']
    P12_MAX= P12_DF['max']
    P12_STD= P12_DF['std']
    P12_OBJ = StatesWeekly(param='P12',count=P12_COUNT,mean=P12_MEAN,min=P12_MIN,max=P12_MAX,std=P12_STD,date=today)
    P12_OBJ.save()

    # For P13 we'll find arithmetic mean
    P13_DF = df['P13'].describe()
    P13_COUNT= P13_DF['count']
    P13_MEAN = P13_DF['mean']
    P13_MIN= P13_DF['min']
    P13_MAX= P13_DF['max']
    P13_STD= P13_DF['std']
    P13_OBJ = StatesWeekly(param='P13',count=P13_COUNT,mean=P13_MEAN,min=P13_MIN,max=P13_MAX,std=P13_STD,date=today)
    P13_OBJ.save()
    
    # For P14 we'll find arithmetic mean
    P14_DF = df['P14'].describe()
    P14_COUNT= P14_DF['count']
    P14_MEAN = P14_DF['mean']
    P14_MIN= P14_DF['min']
    P14_MAX= P14_DF['max']
    P14_STD= P14_DF['std']
    P14_OBJ = StatesWeekly(param='P14',count=P14_COUNT,mean=P14_MEAN,min=P14_MIN,max=P14_MAX,std=P14_STD,date=today)
    P14_OBJ.save()

    # For P15 we'll find arithmetic mean
    P15_DF = df['P15'].describe()
    P15_COUNT= P15_DF['count']
    P15_MEAN = P15_DF['mean']
    P15_MIN= P15_DF['min']
    P15_MAX= P15_DF['max']
    P15_STD= P15_DF['std']
    P15_OBJ = StatesWeekly(param='P15',count=P15_COUNT,mean=P15_MEAN,min=P15_MIN,max=P15_MAX,std=P15_STD,date=today)
    P15_OBJ.save()

    # For P16 we'll find arithmetic mean
    P16_DF = df['P16'].describe()
    P16_COUNT= P16_DF['count']
    P16_MEAN = P16_DF['mean']
    P16_MIN= P16_DF['min']
    P16_MAX= P16_DF['max']
    P16_STD= P16_DF['std']
    P16_OBJ = StatesWeekly(param='P16',count=P16_COUNT,mean=P16_MEAN,min=P16_MIN,max=P16_MAX,std=P16_STD,date=today)
    P16_OBJ.save()