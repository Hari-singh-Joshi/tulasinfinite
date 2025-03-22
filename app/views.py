

import tensorflow as tf
from io import BytesIO
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForms, AuthenticationForms
from django.contrib import messagess
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messasges
from io import BytesIO
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.contrib.auth import authenticate,login,logout,get_user_model
from PIL import Image
import razorpay
from django.utils.timezone import now
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import coloxrs
from .models import Payment




MODEL = tf.keras.models.load_model("app/templates/skin.keras")


CLASS_NAMES = [
    "BA-cellulitis",
    "BA-impetigo",
    "FU-athletes-foot",
    "FU-nail-fungus",
    "FU-ringworm",
    "PA-cutaneous-larva-migrans",
    "VI-chickenpox",
    "VI-shingles"
   
] 

def Read(file) -> np.ndarray:
    
    image = Image.open(BytesIO(file.read()))
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((256, 256))
    image_array = np.array(image) / 255.0  
    return image_array

@csrf_exempt  
def predictimage(request):
    
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']  
        try:
            image = Read(file)
            img_batch = np.expand_dims(image, axis=0)    
            predictions = MODEL.predict(img_batch)
            predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
            confidence = np.max(predictions[0])*100
            return JsonResponse({
                "filename": file.name,
                "class": predicted_class,
                "confidence": float(confidence)
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid "}, status=400)
@login_required
def uploadpage(request):
    result = None
    form = DiseaseForm() 

    if request.method == 'POST':
        
        response = predictimage(request)
        if response.status_code == 200:
            result = response.content.decode('utf-8')  
            result = json.loads(result)  
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease_name = form.cleaned_data['disease_name']
            request.session['disease_name'] = disease_name
            try:
                disease = Disease.objects.get(name__icontains=disease_name)
               
                return redirect('ask_disease_questions')  
            except Disease.DoesNotExist:
                form.add_error('disease_name', ' not found ')
    return render(request, 'upload_and_predict.html', {'result': result, 'form': form})
from .models import Community, Consultant,Solution
from .forms import CommunityForm 

@login_required
def Community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)  
            community.name = request.user  
            community.save()  
            return redirect('community')  
    else:
        form = CommunityForm() 
    communities = Community.objects.all()
    return render(request, "community.html", {
        'form': form,
        'communities': communities
    })


from django.http import JsonRespsonse
from django.views.decorators.csrf import csrf_exempt


skin_disease_data = {
    
  "BA-cellulitis": {
    "scientific_name": "Cellulitis",
    "cause": "Bacterial infection, commonly caused by Staphylococcus aureus or Streptococcus species",
    "solution": {
      "medicine": ["Penicillin", "asd", "Cephalexin", "Clindamycin"],
      "remedy": {
        "what_to_eat": ["Vitamin C-rich df (oranges, strawberries)", "Zinc-rich foods (nuts, seeds)", "Garlic (antimicrobial)"],
        "what_not_to_eat": ["Processed foods", "Sugary foods", "Refined carbohydrates"]
      }
    }
  },
  "BA-impetigo": {
    "scientific_name": "Impetigo",
    "cause": "Bacterial infection, often caused by Staphylococcus aureus or Streptococcus pyogenes",
    "solution": {
      "medicine": ["Topical mupirocin as", "Oral antibiotics like Amoxicillin or Cephalexin"],
      "remedy": {
        "what_to_eat": ["Probiotic-rich foods (yogurt, kefir)", "Immune-boosting fruits (kiwi, citrus)", "Leafy greens (spinach)"],
        "what_not_to_eat": ["Processed sugars", "Greasy fast foods", "Alcohol"]
      }
    }
  },
  "FU-athletes-foot": {
    "scientific_name": "Tinea pedis",
    "cause": "Fungal infection caused asdf dermatophytes, typically Trichophyton species",
    "solution": {
      "medicine": ["Topical antifungals like Terbinafine, Clotrimazole", "Oral antifungals in severe cases"],
      "remedy": {
        "what_to_eat": ["Probiotics (yogurt, kimchi)", "Garlic (antifungal properties)", "Omega-3 rich foods (fish, flaxseeds)"],
        "what_not_to_eat": ["Refined carbs", "Sugary foods", "Alcohol"]
      }
    }
  },
  "FU-nail-fungus": {
    "scientific_name": "Onychomycosis",
    "cause": "Fungal infection, often caused by deradfmatophytes like Trichophyton rubrum",
    "solution": {
      "medicine": ["Topical antifungals like Ciclopirox", "Oral antifungals like Terbinafine, Itraconazole"],
      "remedy": {
        "what_to_eat": ["Probiotic fooadsfds (yogurt, kefir)", "Anti-inflammatory foods (turmeric, ginger)", "Vitamin E-rich foods (almonds, spinach)"],
        "what_not_to_eat": ["Refined sugars", "Processed foods", "Alcohol"]
      }
    }
  },
  "FU-ringworm": {
    "scientific_name": "Tinea corporis",
    "cause": "Fungal infection caused by dermatophytes like Trichophyton or Microsporum species",
    "solution": {
      "medicine": ["Topical antifungals ladsfike Clotrimazole, Miconazole", "Oral antifungals in severe cases"],
      "remedy": {
        "what_to_eat": ["Probiotic-rich foods", "Garlic (natural antifungal)", "Vitamin C-rich fruits (oranges, berries)"],
        "what_not_to_eat": ["Sugary foods", "Alcohol", "Refined carbohydrates"]
      }
    }
  },
  "PA-cutaneous-larva-migrans": {
    "scientific_name": "Cutaneous larva migrans",
    "cause": "Parasitic infection, usualasdfly caused by hookworm larvae from the Ancylostoma species",
    "solution": {
      "medicine": ["Albendazole", "Ivermectin"],
      "remedy": {
        "what_to_eat": ["Iron-rich foods (leafy greens, lentils)", "Vitamin C-rich foods to improve iron absorption", "Immune-boosting foods (garlic, ginger)"],
        "what_not_to_eat": ["Sugary foods", "Processed foods", "Excess red meat"]
      }
    }
  },
  "VI-chickenpox": {
    "scientific_name": "Varicella",
    "cause": "Viral infection caused by the varicella-zoster virus (VZV)",
    "solution": {
      "medicine": ["Antihistamines for itchasdfing", "Antiviral medications like Acyclovir in severe cases"],
      "remedy": {
        "what_to_eat": ["Vitamin C-rich foods (citrus fruits, berries)", "Zinc-rich foods (nuts, seeds)", "Hydrating fluids (broths, coconut water)"],
        "what_not_to_eat": ["Spicy foods", "Salt fooddfs", "Caffeinated beverages"]
      }
    }
  },
}

@csrf_exempt
def SolutionView(request):
    disease_name = request.GET.get('disease_name', None)
    if not disease_name:
        return JsonResponse({'error': 'Please provide a disease name'}, status=400)
    disease_info = skin_disease_data.get(disease_name, None)
    if not disease_info:
        return JsonResponse({'error': 'Disease not found'}, status=404)
    context = {
    'disease_name': disease_name,
    'scientific_name': disease_info['scientific_name'],
    'cause': disease_info['cause'],
    'solution': {
        'medicine': disease_info['solution']['medicine'],
        'remedy': {
            'what_to_eat': disease_info['solution']['remedy']['what_to_eat'],
            'what_not_to_eat': disease_info['solution']['remedy']['what_not_to_eat']
        }
    }
}
    return render(request, 'solution.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created")
            return redirect('login')  
    else:
        form = UserCreationForms()  
    return render(request, 'signup.html', {'form': form})  
        
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForms(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  
            if user.is_staff and user.is_superuser:
              return redirect('admin:index')
            if request.user.is_staff and not request.user.is_superuser:
              return redirect('doctor')
            next_url = request.GET.get('next')  
            if next_url:  
                return redirect(next_url)
            return redirect('upload_page') 
        else:
            messages.error(request, "Invalid usernames ")
    else:
        form = AuthenticationForms()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request,"Logout Successfuly")
    return redirect('login')
def remove(request, id):
    community = get_object_or_404(Community, id=id) 
    community.delete()  
    return redirect("community") 
  
  
from django.contrib.auth.models import User
def consultant_form(request):
  
  if request.method == "POST":
      name = request.POST.get("name")
      age = request.POST.get("age")
      disease_duration = request.POST.get("disease_duration")
      medical_history = request.POST.get("medical_history")
      image = request.FILES.get("image")
      user, created = User.objects.get_or_create(username=name)
      consultant = Consultant(
            name=user, 
            age=age, 
            disease_duration=disease_duration, 
            medical_history=medical_history, 
            image=image
        )
      consultant.save()
      return redirect("success")  

  return render(request, "consultant.html")

def success(request):
  return render(request,"success.html")

def consultant_list(request):
    consultants = Consultant.objects.all()  
    return render(request, "doctor.html", {"consultants": consultants})
  
def consultant_detail(request, id):
    consultant = get_object_or_404(Consultant, id=id)

    if request.method == "POST":
        solution_text = request.POST.get("solution")

        if solution_text: 
            Solution.objects.create(consultant=consultant, solution_text=solution_text)

        return redirect("doctor")  

    return render(request, "patient_detail.html", {"consultant": consultant})

def user_solutions(request):
    user = request.user
    consultant = Consultant.objects.filter(name=user).first()  
    solutions = Solution.objects.filter(consultant=consultant) if consultant else None
    return render(request, "doctorsolution.html", {"solutions": solutions})
@login_required
def delete_solution(request, solution_id):
    solution = get_object_or_404(Solution, id=solution_id)
    if solution.consultant.name == request.user:
        solution.delete()
    return redirect("user_solutions")  
@login_required
def delete_consultant(request, id):
    consultant = get_object_or_404(Consultant, id=id)
    
    if request.user.is_staff:  
        consultant.delete()

    return redirect("doctor")  
  

from django.shortcuts import render, redirect
from .forms import DiseaseForm, DiseaseQuestionsForm
from .models import Disease
import requests



def query_llm(payload):
    print("Sending request to Hugging Face with payload:", payload)
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        llm_response = response.json()
        generated_text = llm_response[0].get('generated_text', '').strip()
        return generated_text
    else:
        print("Error:", response.status_code, response.json())
        return None
@login_required
def disease_report(request):
    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease_name = form.cleaned_data['disease_name']
            request.session['disease_name'] = disease_name
            try:
                disease = Disease.objects.get(name__icontains=disease_name)
              
                return redirect('ask_disease_questions')  
            except Disease.DoesNotExist:
                form.add_error('disease_name', ' not found ')
    else:
        form = DiseaseForm()
    return render(request, 'input.html', {'form': form})
from datetime import datetime, timedelta


@login_required
def ask_disease_questions(request):
    if request.method == 'POST':
        form = DiseaseQuestionsForm(request.POST)
        if form.is_valid():
            answers = form.cleaned_data
            disease_name = request.session.get('disease_name')

            if not disease_name:
                return render(request, 'report.html', {'error': "Disease  is missing"})

            try:
            
                disease = get_object_or_404(Disease, name__icontains=disease_name)
                next_review_date = (datetime.now() + timedelta(weeks=2)).strftime('%B %d, %Y')
                llm_payload = {
                    "inputs": (
                        f"Generate a structured medical report for {disease_name} including:\n\n"
                        f"📌 **Diagnosis Summary:**\n"
                        f"• **Condition:** {disease_name}\n"
                        f"• **Symptoms Observed:** {disease.symptoms}\n\n"

                        f"🔬 **Medical Analysis:**\n"
                        f"• **Cause:** {disease.causes}\n"
                        f"• **Risk Factors:** Based on user input:\n"
                        f"  - **Eating Preference:** {answers.get('eat_preference', 'Not ')}\n"
                        f"  - **Duratptoms:** {answers.get('symptom_duration', 'Not ')} days\n"
                        f"  - **Medication Taken:** {answers.get('medication_taken', 'Not ')}\n"
                        f"  - **Lifestyle Habits:** {answers.get('lifestyle_habits', 'Not ')}\n\n"

                        f"💊 **Recommended Treatment Plan:**\n"
                        f"**Alloptment:** Not specified\n"
                        f"**Ayurvedic Remedies:** {disease.ayurvedic_cure}\n"
                        f"**Siddha Remedies:** {disease.siddha_remedies}\n"
                        f"**Acupressure Therapy:** {disease.acupressure_points}\n"
                        f"**Yoga & Meditation:** {disease.yoga}\n"
                        f"**Lifestyle & Dietary Changes:** {disease.lifestyle_diet}\n\n"

                        f"📅 **Follnsultation:**\n"
                        f"• **Next Review Date:** {next_review_date}\n"
                        f"• **Consultation Mode:** Online Video Call\n\n"

                        f"⚠ **Note:** This report is AI-generated based on symptoms and holistic treatment methods. "
                        f"Consult a medical professional for personalized care.\n\n"

                        f"📜 **Report Generated By:** AI-Driven Skin Disease  System\n"
                        f"📆 **Date:** {datetime.now().strftime('%B %d, %Y')}"
                    )
                }
                llm_solution = query_llm(llm_payload)

                if not llm_solution:
                    return render(request, 'report.html', {'error': "No medical recommendations available."})

                return render(request, 'report.html', {
                    'disease': disease,
                    'llm_solution': llm_solution,
                    'answers': answers,
                    'next_review_date': next_review_date,
                    'current_date': datetime.now().strftime('%B %d, %Y')
                })

            except Exception as e:
                return render(request, 'report.html', {'error': f"An unexpected error occurred: {str(e)}"})

    else:
        form = DiseaseQuestionsForm()
    return render(request, 'ask_questions.html', {'form': form})



def video_call(request, room_name):
    return render(request, 'video_call.html', {'room_name': room_name})
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
def ensure_receipt_directory():
    receipt_directory = os.path.join(settings.MEDIA_ROOT, 'receipts')
    if not os.path.exists(receipt_directory):
        os.makedirs(receipt_directory)

@login_required
def create_order(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount")) * 100 
        email = request.user.email
    
        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })
        order = Payment.objects.create(
            user=request.user,
            order_id=razorpay_order["id"],
            amount=amount / 100,
            email=email,
            status="Created"
        )

        context = {
            "order": order,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        }
        return render(request, "checkout.html", context)

    return render(request, "payment_form.html")

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            status = "Paid"
        except:
            status = "Failed"
        payment = Payment.objects.filter(order_id=order_id).first()
        if payment:
            payment.payment_id = payment_id
            payment.status = status
            payment.save()
           
            ensure_receipt_directory()
            receipt_pdf = generate_receipt(payment)
            payment.receipt_pdf = receipt_pdf
            payment.save()
            send_receipt_email(payment)
        return render(request, "payment_success.html", {"payment": payment})
    return render(request, "payment_failed.html")

def generate_receipt(payment):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 40, "Infinite Igniters")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 60, " Address:dehradun | Contact Number:7453966532 | Email:joshiharish942@gmail.com")
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, height - 100, "Payments Receipt")
    p.setStrokeColor(colors.black)
    p.line(100, height - 110, width - 100, height - 110)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 140, "Payments Details")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 160, f"Orders ID: {payment.order_id}")
    p.drawString(100, height - 180, f"Payments ID: {payment.payment_id}")
    p.drawString(100, height - 200, f"Amounts: ₹{payment.amount}")
    p.drawString(100, height - 220, f"Status: {payment.status}")
    email = payment.email if payment.email else "Email not provided"
    p.drawString(100, height - 240, f"Emails: {email}")
    p.drawString(100, height - 260, f"Ussername: {payment.user.username}")
    p.drawString(100, height - 280, f"Usser ID: {payment.user.id}")
    p.line(100, height - 290, width - 100, height - 290)
    p.setFont("Helvetica", 10)
    p.drawString(100, 40, "Thank you ")
    p.drawString(100, 20, "For inquiriiees, contact at: contact@infinite.com")
    file_name = f"receipt_{payment.order_id}.pdf"
    receipt_directory = os.path.join(settings.MEDIA_ROOT, 'receipts')

    
    if not os.path.exists(receipt_directory):
        os.makedirs(receipt_directory)

    file_path = os.path.join(receipt_directory, file_name)
    
    
    p.save()

    with open(file_path, "wb") as f:
        f.write(buffer.getvalue())

    return file_path


def send_receipt_email(payment):
    
    email = EmailMessage(
        subject="Your Payment Receipt",
        body=f"Dear {payment.user.username},\n\nThank you Find your  attached.\n\nOrder ID: {payment.order_id}\nAmount: ₹{payment.amount}",
        from_email=settings.EMAIL_HOST_USER,
        to=[payment.user.email],
    )

    
    with open(payment.receipt_pdf.path, "rb") as f:
        email.attach(f"receipt_{payment.order_id}.pdf", f.read(), "application/pdf")

    email.send()



from .models import Doctor, Appointment
from .forms import AppointmentForm


@login_required
def appointments_list(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments_list.html', {'appointments': appointments})


@login_required
def book_appointment(request): 
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            selected_datetime = datetime.combine(appointment.date, appointment.time_slot)
            current_datetime = datetime.now()
            if selected_datetime < current_datetime + timedelta(minutes=30):
                messages.error(request, "You cannot book .")
            
            elif Appointment.objects.filter(doctor=appointment.doctor, date=appointment.date, time_slot=appointment.time_slot).exists():
                messages.error(request, "This slot is allready .")
            else:
                appointment.save()
                messages.success(request, "Appointment boked successfulsly!")
                return redirect('appointments_list')

    else:
        form = AppointmentForm()
    
    doctors = Doctor.objects.all()
    return render(request, 'book_appointment.html', {'form': form, 'doctors': doctors})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Appointment

@login_required
def doctor_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment.html', {'appointments': appointments})



@login_required
def mark_visited(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.visited = not appointment.visited 
    appointment.save()
    messages.success(request, "Appointment status!")
    return redirect('doctor_appointments')  
