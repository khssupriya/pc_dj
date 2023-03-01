from rest_framework import serializers

from .models import Patient, Sample

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = (
            "id",
            "owner",
            "patient",
            "date_collected",
            "diagnosis_code",
            "type",
            "origin",
            "symptoms",
            "comments",
            "get_image",
            "get_thumbnail",
            "predicted_label",
            "human_label",
        )

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "name",
            "sex",
            "dob",
            "phone_number",
        )
        