from django.shortcuts import render
from datetime import datetime,timedelta
from .models import SerialCommunication,Averages
import pandas as pd
from scipy.stats import circmean
from django.http import JsonResponse
from decimal import Decimal

# Create your views here.

def set_yesterday_average(request):
    current_date = datetime.now().date()
    yesterday_date = (current_date - timedelta(days=1))
    objs = list(SerialCommunication.objects.filter(RTC__date = yesterday_date).values())
    print(objs)
    if(not objs):        
        JsonResponse({'status':True})
    df = pd.DataFrame(objs).apply(pd.to_numeric,errors='coerce', downcast='float').round(3)

    # For WSPD we'll find arithmetic mean
    WSPD_MEAN = Decimal(str(df["WSPD"].mean()))
    WDIR_MEAN = Decimal(str(round(circmean(df['WDIR'], high=360, low=0),3)))
    ATMP_MEAN = Decimal(str(df['ATMP'].mean()))
    HUMD_MEAN = Decimal(str(df['HUMD'].mean()))
    RAIN_MEAN = Decimal(str(df['RAIN'].sum()))
    SRAD_MEAN =  Decimal(str(df['SRAD'].mean()))
    BPRS_MEAN =  Decimal(str(df['BPRS'].mean()))
    WDCH_MEAN = Decimal(str(df['WDCH'].mean()))
    DWPT_MEAN =  Decimal(str(df['DWPT'].mean()))

    avg_obj = Averages(date=yesterday_date,WSPD=WSPD_MEAN,WDIR=WDIR_MEAN,ATMP=ATMP_MEAN,HUMD=HUMD_MEAN,RAIN=RAIN_MEAN,SRAD=SRAD_MEAN,BPRS=BPRS_MEAN,WDCH=WDCH_MEAN,DWPT=DWPT_MEAN)
    avg_obj.save()
    return JsonResponse({'status':True})