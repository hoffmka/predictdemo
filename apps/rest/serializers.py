from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    project = serializers.CharField()
    targetId = serializers.CharField()
    status = serializers.CharField()
    magpieJobId = serializers.IntegerField()
    url = serializers.CharField()