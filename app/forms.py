from django import forms
from .models import Community

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['box']
        labels = {
            'box': 'Community Description',  
        }
        widgets = {
            'box': forms.Textarea(attrs={
                'placeholder': 'Enter community description here...',
                'rows': 4, 
                'class': 'form-control' 
            }),
        }

    def clean_box(self):
        data = self.cleaned_data['box']
        if len(data) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return data




class DiseaseForm(forms.Form):
    DISEASE_CHOICES = [
        ('Acne', 'Acne'),
        ('Actinic Carcinoma', 'Actinic Carcinoma'),
        ('Atopic Dermatitis (Eczema)', 'Atopic Dermatitis (Eczema)'),
        ('Bullous Disease', 'Bullous Disease'),
        ('Drug Eruptions', 'Drug Eruptions'),
        ('Herpes (HPV)', 'Herpes (HPV)'),
        ('Lupus', 'Lupus'),
        ('Melanoma', 'Melanoma'),
        ('Poison Ivy', 'Poison Ivy'),
        ('Psoriasis', 'Psoriasis'),
        ('Benign Tumors', 'Benign Tumors'),
        ('Systemic Disease', 'Systemic Disease'),
        ('Urticarial Hives', 'Urticarial Hives'),
        ('Viral Rashes', 'Viral Rashes'),
        ('Viral Infection - Shingles (Herpes Zoster)', 'Viral Infection - Shingles (Herpes Zoster)'),
        ('Viral Infection - Chickenpox', 'Viral Infection - Chickenpox'),
        ('Parasitic Infections - Cutaneous Larva Migrans', 'Parasitic Infections - Cutaneous Larva Migrans'),
        ('Fungal Infections - Ringworm', 'Fungal Infections - Ringworm'),
        ('Fungal Infections - Nail Fungus', 'Fungal Infections - Nail Fungus'),
        ('Fungal Infections - Athlete’s Foot', 'Fungal Infections - Athlete’s Foot'),
        ('Bacterial Infections - Impetigo', 'Bacterial Infections - Impetigo'),
        ('Bacterial Infections - Cellulitis', 'Bacterial Infections - Cellulitis'),
    ]
    
    disease_name = forms.ChoiceField(
    choices=DISEASE_CHOICES,
    label='Select a Disease',
    widget=forms.Select(attrs={'class': 'form-control w-100'})
)





from django import forms
from django import forms

class DiseaseQuestionsForm(forms.Form):
  
    FOOD_CHOICES = [
        ("vegetarian", "Vegetarian"),
        ("non_vegetarian", "Non-Vegetarian"),
        ("vegan", "Vegan"),
        ("balanced", "Balanced Diet"),
        ("other", "Other"),
    ]
    eat_preference = forms.ChoiceField(
        choices=FOOD_CHOICES,
        required=True,
        label="What type of food do you prefer?",
        help_text="Choose the option that best matches your diet.",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    symptom_duration = forms.IntegerField(
        min_value=1,
        max_value=365,  
        required=True,
        label="How long have you been experiencing symptoms (in days)?",
        help_text="Enter a number between 1 and 365.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10'}),
    )

   
    medication_taken = forms.CharField(
        max_length=500,
        required=False,
        label="Have you taken any medications?",
        help_text="List any medications taken or type 'None'.",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List any medications...'}),
    )

  
    lifestyle_habits = forms.CharField(
        max_length=500,
        required=True,
        label="Describe your lifestyle habits (exercise, smoking, alcohol, etc.)",
        help_text="Provide details about your daily activities and habits.",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your lifestyle habits...'}),
    )
    age = forms.IntegerField(
    required=True,
    label="Enter Your Age",
    widget=forms.NumberInput(attrs={'class': 'form-control'}),
)



from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time_slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
        }