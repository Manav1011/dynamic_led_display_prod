from .models import States
from rest_framework import serializers

class DailyAverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ['param','mean']