from django.urls import path
from . import views


urlpatterns=[
    path('tl',views.TimeLeft.as_view()),
    path('verify_token',views.VerifyToken.as_view()),
    path('register',views.RegisterView.as_view()),
    path('login',views.LoginView.as_view()),
    path('get_access_token',views.GetAccessToken.as_view()),
    path('student/<int:std_id>',views.GetStudentDetails.as_view()),
    path('fetch_qr',views.MakePayment.as_view()),
    path('make_payment',views.MakePayment.as_view()),
    path('verify_email',views.VerifyEmail.as_view()),
    path('subscribe',views.Subscribe.as_view()),
    path('action',views.Action.as_view()),
    path('workshop/<str:secret>',views.GetExcel().as_view()),
    path('contest/<str:secret>',views.GetExcel().as_view()),
]