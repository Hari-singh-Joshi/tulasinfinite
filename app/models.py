from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()  

class Community(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)  
    box = models.TextField(max_length=500)  

    def __str__(self):
        return self.name.username  
    
class Consultant(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    disease_duration = models.PositiveBigIntegerField()
    medical_history = models.TextField()
    image = models.ImageField(upload_to='disease/')
    
    def __str__(self):
        return self.name.username
class Solution(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    solution_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Disease(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    symptoms = models.TextField()
    causes = models.TextField()
    ayurvedic_cure = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    yoga = models.TextField(blank=True, null=True)
    siddha_remedies = models.TextField(blank=True, null=True)
    acupressure_points = models.TextField(blank=True, null=True)
    lifestyle_diet = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField(default=100,editable=False)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=50, default="Created")
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    receipt_pdf = models.FileField(upload_to="receipts/", blank=True, null=True)

    def __str__(self):
        return f"Payment {self.order_id} - {self.status}"
    


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return self.name


    
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()
    booked_at = models.DateTimeField(auto_now_add=True)
    visited = models.BooleanField(default=False)  

    class Meta:
        unique_together = ('doctor', 'date', 'time_slot') 

    def __str__(self):
        status = "Visited" if self.visited else "Not Visited"
        return f"{self.patient.username} - {self.doctor.name} at {self.time_slot} ({status})"