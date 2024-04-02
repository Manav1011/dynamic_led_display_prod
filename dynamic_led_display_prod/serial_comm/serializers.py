from .models import Averages,States,StatesWeekly
from rest_framework import serializers

class DailyAverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Averages
        fields = ['ATMP','BPRS','DWPT','HUMD','RAIN','SRAD','WDCH','WDIR','WSPD']

class DailyStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ['param','count','mean','min','max','std','date','created_at']

class WeeklyStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatesWeekly
        fields = ['param','count','mean','min','max','std','date','created_at']