from allauth.account.forms import SignupForm, LoginForm


class CustomSigninForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'col l7 push-l1 s12 form-input',
            'required': 'required'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'col l7 push-l1 s12 form-input',
            'required' : 'required'
        })