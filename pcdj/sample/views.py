import json
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Patient, Sample, SharedComment
from .serializers import PatientSerializer, SampleSerializer, SharedCommentSerializer
from .utils import model_predict

# from django.contrib.auth import User

class SamplesList(APIView):
    parser_classes = [MultiPartParser, FileUploadParser]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        samples = Sample.objects.filter(owner=self.request.user).all()
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = SampleSerializer(data=request.data, context={'request': request})
        # print(serializer.is_valid(), serializer.data, "sseeeee")
        if serializer.is_valid():
            sample = serializer.save(owner=request.user)
            if 'image' in request.data:
                sample.image = request.data['image']
                sample.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PatientsList(APIView):
    parser_classes = [MultiPartParser, FileUploadParser]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        samples = Patient.objects.all()
        serializer = PatientSerializer(samples, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone_number')
        data = {
            'name': name,
            'sex': sex,
            'dob': dob,
            'phone_number': phone_number,
        }
        serializer = PatientSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            patient = serializer.save()
            return Response(patient.id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SharedCommentsList(APIView):
    # parser_classes = [MultiPartParser, FileUploadParser]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # reeciver makes the call here to get all sharedComments shared with them
        sharedComments = SharedComment.objects.filter(receiver=self.request.user).all()
        serializer = SharedCommentSerializer(sharedComments, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if(SharedComment.objects.filter(receiver=request.data["receiver"], sample=request.data["sample"]).exists()):
            return Response("Already shared", status=status.HTTP_400_BAD_REQUEST)
        # sender makes the call to create a new SharedComment
        serializer = SharedCommentSerializer(data=request.data, context={'request': request})
        # print(serializer.is_valid(), serializer.data, "sseeeee")
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SampleDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, sample_id):
        try:
            return Sample.objects.get(id=sample_id)
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

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def predict_sample(request):
    try:
        sample_id = request.data.get('sample_id', '')
        try:
            print(Sample.objects.filter(owner=request.user), sample_id)
            sample = Sample.objects.get(id=sample_id)
            prediction = model_predict(sample.image)
            sample.predicted_label = prediction
            sample.save(update_fields=['predicted_label'])
            serializer = SampleSerializer(sample)
            return Response(serializer.data)
        except Sample.DoesNotExist:
            raise Http404
    except AttributeError:
        return Response("sample_id is missing in request", status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def predict_image(request):
    try:
        image = request.data.get('image', '')
        prediction = model_predict(image)
        return Response({"predictedLabel": prediction})
    except AttributeError:
        return Response("image is missing in request", status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_annotations(request):
    sample_id = request.data.get('sample_id', '')
    annotations = request.data.get('annotations', '')
    try:
        sample = Sample.objects.filter(owner=request.user).get(id=sample_id)
        sample.annotations = annotations
        sample.save(update_fields=['annotations'])
        serializer = SampleSerializer(sample)
        return Response(serializer.data)
    except Sample.DoesNotExist:
        raise Http404
    

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_receiver_comment(request):
    shared_comment_id = request.data.get('shared_comment_id', '')
    receiver_comment = request.data.get('receiver_comment', '')
    try:
        shared_comment = SharedComment.objects.get(id=shared_comment_id)
        shared_comment.receiver_comment = receiver_comment
        shared_comment.status = 'complete'
        shared_comment.save(update_fields=['receiver_comment', 'status'])
        serializer = SharedCommentSerializer(shared_comment)
        return Response(serializer.data)
    except SharedComment.DoesNotExist:
        raise Http404
    

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_sample_shared_comments(request):
    sample_id = request.data.get('sample_id', '')
    try:
        shared_comments = SharedComment.objects.filter(sample=sample_id)
        print(shared_comments)
        if(shared_comments):
            serializer = SharedCommentSerializer(shared_comments, many=True)
            return Response(serializer.data)
        return Response({"message": "empty"})
    except SharedComment.DoesNotExist:
        raise Http404
    

# @api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def get_username(request):
#     user_id = request.data.get('user_id', '')
#     try:
#         user = User.objects.filter(sample=sample_id)
#         print(user)
#         return Response({"user": "username"})
#     except SharedComment.DoesNotExist:
#         raise Http404

# create Profile object
        