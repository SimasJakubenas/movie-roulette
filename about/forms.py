from .models import ContactFormModel
from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormModel
        fields = ('name', 'email', 'message')

    # def save(self, *args, **kwargs):

    #     conntact_form = super().save(*args, **kwargs)
    #     form_entry = ContactFormModel.objects.create(
    #         name=self.cleaned_data.get("name"),
    #         email=self.cleaned_data.get("email"),
    #         message=self.cleaned_data.get("message")
    #     )

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
