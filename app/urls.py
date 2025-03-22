from django.urls import path, include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import video_call

urlpatterns = [
    path('doctorss/', views.doctor_appointments, name='doctor_appointments'),
    path('mark-visited/<int:appointment_id>/', views.mark_visited, name='mark_visited'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path("pay/", views.create_order, name="pay"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path('call/<str:room_name>/', video_call, name='video_call'),
    path('report/', views.disease_report, name='disease_report'),
    path('ask/', views.ask_disease_questions, name='ask_disease_questions'),
    path('upload/', views.upload_page, name='upload_page'),
    path('success/', views.success, name="success"),
    path('doctor/', views.consultant_list, name="doctor"),
    path('consultant/delete/<int:id>/', views.delete_consultant, name='delete_consultant'),
    path('consultants/<int:id>/', views.consultant_detail, name="patient_detail"),
    path('consultant/', views.consultant_form, name="consultant"),
    path('my-solutions/', views.user_solutions, name="user_solutions"),
    path('solution/delete/<int:solution_id>/', views.delete_solution, name='delete_solution'),
    path('solution/', views.SolutionView, name='solution'),
    path('predict/', views.predictimage, name='predict_image'),
    path("signup/", views.signup_view, name="signup"),
    path("", views.login_view, name="login"),  
    path("logout/", views.logout_view, name="logout"),
    path("community/", views.CommunityView, name="community"),
    path('remove/<int:id>/', views.remove, name='delete'),
    path('auth/', include('social_django.urls', namespace='social')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)










