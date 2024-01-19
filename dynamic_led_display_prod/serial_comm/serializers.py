from .models import Averages
from rest_framework import serializers

class DailyAverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Averages
        fields = ['ATMP','BPRS','DWPT','HUMD','RAIN','SRAD','WDCH','WDIR','WSPD']