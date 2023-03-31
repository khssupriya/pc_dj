from rest_framework import serializers

from .models import Patient, Sample, SharedComment

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = (
            "id",
            "owner",
            "patient",
            "date_collected",
            "date_added",
            "diagnosis_code",
            "type",
            "origin",
            "symptoms",
            "comments",
            "get_image",
            "get_thumbnail",
            "predicted_label",
            "human_label",
            "annotations"
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

class SharedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedComment
        fields = (
            "id",
            "status",
            "sample",
            "sender",
            "receiver",
            "sender_comment",
            "receiver_comment",
        )
        