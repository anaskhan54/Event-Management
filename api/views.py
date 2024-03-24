from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .functions import verify_recaptcha
from .models import Students
import re

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        try:
            recaptcha_response=request.POST.get('g-recaptcha-response')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_number = request.POST.get('mobile_number')
            gender = request.POST.get('gender')
            college_email = request.POST.get('college_email')
            student_id = request.POST.get('student_id')
            branch = request.POST.get('branch')
            section = request.POST.get('section')
            is_hosteler = request.POST.get('is_hosteler')
            hacker_rank_id = request.POST.get('hacker_rank_id')
        except:
             return Response({"message":"Some fields are missing"},status=400)
        if (verify_recaptcha(recaptcha_response)):
             pass
        else:
            return Response({'message':'Invalid Recaptcha'},status=400)
        if not re.match(r'^[a-zA-Z0-9_.+-]+@akgec\.ac\.in$', college_email):
             
             if student_id not in college_email:
                return Response({"message":"Only first year students are allowed"},status=400)
             return Response({"message":"Only College email is allowed"},status=400)
        if not re.match(r'^[a-zA-Z]+$', first_name):
            return Response({"message":"First name is invalid"},status=400)
        if not re.match(r'^[a-zA-Z]+$', last_name):
            return Response({"message":"Last name is invalid"},status=400)
        if not re.match(r'^[0-9]{10}$', mobile_number):
            return Response({"message":"Mobile number is invalid"},status=400)
        if not re.match(r'^23[0-9]+$', student_id):
            return Response({"message":"Only first year students are allowed"},status=400)
        if is_hosteler=="on":
                    is_hosteler=True
        else:
            is_hosteler=False
        
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
        return Response({'message':'Registered Successfully'},status=201)
      
        