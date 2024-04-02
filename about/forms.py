from .models import ContactFormModel
from django import forms


class ContactForm(forms.ModelForm):
    """
    Model for the form to contact the admin
    """
    class Meta:
        model = ContactFormModel
        fields = ('name', 'email', 'message')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-input'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input'
        })
        self.fields['message'].widget.attrs.update({
            'class': 'form-input',
            'rows': '5'
        })
