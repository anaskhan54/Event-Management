from django.urls import path
from . import views

urlpatterns=[
    path('/register',views.RegisterView.as_view()),
    path('/login',views.LoginView.as_view()),
    path('/get_access_token',views.GetAccessToken.as_view()),
    path('/student/<int:std_id>',views.GetStudentDetails.as_view()),
    path('/make_payment',views.MakePayment.as_view()),
    
]