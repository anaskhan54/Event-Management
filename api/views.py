from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .functions import verify_recaptcha,send_qr_code,generate_tokens, is_refresh_valid, is_access_valid,decrypt_data,time_left
from .models import Students,Coordinators
import re
import hashlib
import jwt
from rest_framework import serializers
from .serializers import StudentSerializer

# Create your views here.

class TimeLeft(APIView):
    def get(self,request):
        target_date = "01/04/2024 00:00"
        days, hours, minutes, seconds = time_left(target_date)
        return Response({"days":days,"hours":hours,"minutes":minutes,"seconds":seconds},status=200)
class RegisterView(APIView):
    def post(self,request):
        
        try:
            #recaptcha_response= request.headers.get('Recaptcha-Token')
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            mobile_number = request.data['mobile_number']
            gender = request.data['gender']
            college_email = request.data['college_email']
            student_id = request.data['student_id']
            branch = request.data['branch']
            section = request.data['section']
            is_hosteler = request.data['is_hosteler']
            hacker_rank_id = request.data['hacker_rank_id']
        except:
             return Response({"message":"Some fields are missing"},status=400)
        recaptcha_response="papa"
        if (verify_recaptcha(recaptcha_response)) or True:
             pass
        else:
            return Response({'message':'Invalid Recaptcha'},status=400)
        if(settings.PRODUCTION=="TRUE"):
             
            if not re.match(r'^[a-zA-Z0-9_.+-]+@akgec\.ac\.in$', college_email):
                return Response({"message":"Only College email is allowed"},status=400)
            if student_id not in college_email:
                return Response({"message":"Only first year students are allowed"},status=400)
            if not re.match(r'^[a-zA-Z\s]+$', first_name):
                return Response({"message":"First name is invalid"},status=400)
            if not re.match(r'^[a-zA-Z\s]+$', last_name):
                return Response({"message":"Last name is invalid"},status=400)
            if not re.match(r'^[0-9]{10}$', mobile_number):
                return Response({"message":"Mobile number is invalid"},status=400)
            if not re.match(r'^23[0-9]+$', student_id):             
                return Response({"message":"Only first year students are allowed"},status=400)
        
        if is_hosteler=="on":
                    is_hosteler=True                
        else:
            is_hosteler=False 
        
        #check if user already registered
            
        send_qr_code(college_email,student_id)
        
            
        student = Students(
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                gender=gender,
                college_email=college_email,
                student_id=student_id,
                branch=branch,
                section=section,
                isHosteler=is_hosteler,
                hacker_rank_id=hacker_rank_id
            )
        student.save()
        return Response({'message':'Registered Successfully, Check Your E-mail'},status=201)
      
        
        
class LoginView(APIView):
     def post(slef,request):
        print(request.data)
        try:
            username = request.data['username']
            password = request.data['password']
            
        except:
            return Response({"message":"Some fields are missing"},status=400)
        try:
            coordinator = Coordinators.objects.get(username=username)
        except:
            return Response({"message":"Invalid Credentials"},status=400)
        if coordinator.password==hashlib.sha256(password.encode()).hexdigest():
            access_token, refresh_token = generate_tokens(coordinator.id)
            response_data={
                'access_token':access_token,
                'refresh_token':refresh_token,
                'username':coordinator.username
            }
            return Response(response_data,status=200)
        else:
            return Response({"message":"Invalid Credentials"},status=400)
        
class GetAccessToken(APIView):
    def get(self,request):
        try:
            refresh_token = request.data['refresh_token']
        except:
            return Response({"message":"No refresh token in body"},status=400)
        if(is_refresh_valid(refresh_token)):
            id=jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=['HS256'])['id']
            access_token, refresh_token = generate_tokens(id)
            return Response({"access_token":access_token},status=200)
        else:
            return Response({"message":"Either the token is invalid or expired"},status=400)



class GetStudentDetails(APIView):
    def get(self,request,std_id):
        try:
            token=request.headers['Authorization']
            if(is_access_valid(access_token=token)):
                pass
            else:
                return Response({"message":"Either the token is expired or is invalid"},status=400)
            
        except:
            return Response({"message":"Unauthorized"},status=401)
        
        try:
            student=Students.objects.filter(student_id=std_id).first()

            serializer = StudentSerializer(student)
            
            return Response(serializer.data,status=200)
        except Exception as e:
            return Response({"message":"student not found"},status=404)

class MakePayment(APIView):
    def post(self,request):
        try:
            token=request.headers['Authorization']
            if(is_access_valid(access_token=token)):
                pass
            else:
                return Response({"message":"Either the token is expired or is invalid"},status=400)
            
        except:
            return Response({"message":"Unauthorized"},status=401)
        
        try:
            qr_data=request.data['qr_data']
            try:
                std_id=decrypt_data(qr_data)
                student=Students.objects.get(student_id=std_id).first()
                if(student.isPaid):
                    return Response({"message":"Already Paid"},status=200)
                else:
                    student.isPaid=True
                    student.save()
                    serializer=StudentSerializer(student)
                    return Response({"message":"Payment Successful",
                                     "student_details":serializer.data},status=200)
            except:
                return Response({"message":"Invalid QR Code"},status=400)
        except:
            return Response({"message":"No qr_data in body"},status=400)
        