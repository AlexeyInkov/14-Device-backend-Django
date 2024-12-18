from rest_framework import serializers


class MySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
