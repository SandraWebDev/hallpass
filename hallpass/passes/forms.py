from django import forms
from django.forms import ModelForm
from .models import Student, HallPass, Destination, Category, Profile
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError





class LogForm(forms.Form):
    log_id = forms.CharField() # This is all we need to get cleaned_data from the form


    
class ArrivalForm(forms.Form):
    student_id = forms.CharField(max_length=6)
    destination_id = forms.CharField() # This is all we need to get cleaned_data from the form
    
    
    def clean_student(self):
        input_id = self.cleaned_data["student"]
        id_length = len(input_id)
        validate = []

        if id_length != 6:
            validate.append("must be 6 numbers /b")
            
        if not input_id.isnumeric():
            validate.append("Student Id's don't contain letters")
            
        # student_query = Student.objects.filter(student_id=input_id)
        # if len(student_query) <= 0:
        #     validate += "Must be a valid student ID"
        #     raise ValidationError(validate.split("/b"))

        if Student.objects.filter(student_id=input_id).exists():
            validate.append("This ID does not exist")

        # We can let kids go to the 
        # bathroom if they are from another school 
        # if student_query[0].building != self.request.user.profile.building:
        #     validate += "Student must belong to current building"
            
        if (len(validate) > 0):
            raise ValidationError(validate)
        

        return input_id
    
class ProfileForm(forms.ModelForm):
    destinations_choices = None
    destinations = forms.ModelMultipleChoiceField(
        label='Destinations', 
        queryset=destinations_choices, 
        required=False, 
        widget=forms.CheckboxSelectMultiple()
    )
    destinations.widget.template_name = 'widgets/destination_choices.html'

    class Meta:
        model = Profile
        fields = ('building','destinations',)
        widgets = {
            'building': forms.Select(attrs={'onchange':'this.form.submit()'}) # This isn't best practice. We should use JS for this.
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Order_by sorts the choices by alpha.
        self.destinations_choices = Destination.objects.filter(building = self.instance.building).order_by('room', 'category')
        self.fields['destinations'].queryset = self.destinations_choices
        self.fields['building'].label="Buildings"


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
            'text_color': TextInput(attrs={'type': 'color'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())
