from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Patient, Sample
from .serializers import PatientSerializer, SampleSerializer

class SamplesList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        samples = Sample.objects.filter(owner=self.request.user).all()
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    
class SampleDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, sample_id):
        try:
            return Sample.objects.filter(owner=self.request.user).get(id=sample_id)
        except Sample.DoesNotExist:
            raise Http404
        
    def get(self, request, sample_id, format=None):
        sample = self.get_object(sample_id=sample_id)
        serializer = SampleSerializer(sample)
        return Response(serializer.data)
    
class PatientDetail(APIView):
    def get_object(self, patient_id):
        try:
            return Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise Http404
        
    def get(self, request, patient_id, format=None):
        patient = self.get_object(patient_id=patient_id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def search(request):
    query = request.data.get('query', '')

    if query:
        samples = Sample.objects.filter(owner=request.user).filter(
            Q(patient__name__icontains=query) |
            Q(origin__contains=query) |
            Q(type__icontains=query) |
            Q(predicted_label__icontains=query) |
            Q(human_label__icontains=query) |
            Q(comments__icontains=query) |
            Q(symptoms__icontains=query) 
        )
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    else:
        return Response({"samples": []})
