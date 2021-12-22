from django import forms

class Login(forms.Form):
    email = forms.CharField(max_length=400, widget=forms.TextInput(attrs={'placeholder':'Enter Username'}))
    passwd = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Password'}))

Gender_choice= [
    ('male', 'Male'),
    ('female', 'Female')
    ]


class Signup(forms.Form):
    
    firstname = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder':'Enter your firstname','required':True}))
    lastname = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder':'Enter your lastname','required':True}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter your email','required':True,'required':True}))
    passwd = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'placeholder':'Enter a password','required':True,'required':True}))
    cpasswd = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'placeholder':'Retype password','required':True,'required':True}))
    phone=forms.IntegerField()
    gender=forms.CharField(label='Gender', widget=forms.RadioSelect(choices=Gender_choice))


class Otp(forms.Form):
    email = forms.EmailField()

class CheckOtp(forms.Form):
    otp = forms.CharField(max_length=4)

class changepassword(forms.Form):
    password = forms.CharField(max_length=50,widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=50,widget=forms.PasswordInput)

mealschoice=[
    ('yes', 'Yes'),
    ('no', 'No')
]

AREACHOICE=[
     ('Malviya nagar', 'Malviya nagar'),
    ('gopalpura', 'Gopalpura')
]

class Roompost(forms.Form):
    description = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder':'Enter your firstname','required':True}))
    area= forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=AREACHOICE))
    zipcode =forms.CharField(max_length=10)
    rent=forms.CharField(max_length=10)
    facilities=forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder':'TV,WIFI etc','required':True}))
    meals=forms.CharField(label='Meals Included', widget=forms.RadioSelect(choices=mealschoice))
    name=forms.EmailField(max_length=40, widget=forms.TextInput(attrs={'placeholder':'Enter your email','required':True}))
    contact=forms.CharField(max_length=10)
    roompic =forms.ImageField()


class Contact(forms.Form):
    name = forms.CharField(max_length=40)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)