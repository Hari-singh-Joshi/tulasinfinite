from django.contrib import admin
from .models import Consultant,Solution,Disease,Payment,Doctor,Appointment

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('id', 'age', 'disease_duration', 'medical_history')
    search_fields = ('age', 'medical_history')
    list_filter = ('age', 'disease_duration')

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    
@admin.register(Disease)
class SolutionAdmin(admin.ModelAdmin):
    list_filter = ('code',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "order_id", "payment_id", "amount", "status", "created_at")
    list_filter = ("status", "created_at",'user')
    search_fields = ("order_id", "payment_id", "user__username", "user__email", "user__parent__full_name")  
    
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_filter = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_filter = ('booked_at',)