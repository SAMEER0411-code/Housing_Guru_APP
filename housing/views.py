from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import Login,Signup,Otp,CheckOtp,changepassword,Roompost,Contact
from .models import user,postmodel
from django.views import View
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import hashers
# Create your views here.
def index(request):
    if request.session.get('email'):
        return render(request,"afterlogin.html")
    else:
        return render(request,"index.html")

def login(request):
    if request.session.get('islogin'):
        error = "Already logged in"
        return render(request,"afterlogin.html",{'error':error})
    else:
        return render(request,"index.html")

def login1(request):
    #return render(request,"login.html")
    form=Login(request.POST)
    if form.is_valid():
        if request.method =="POST":
            email=form.cleaned_data['email']
            try:
                user.objects.get(email=email)
            except user.DoesNotExist as e:
                error = "User does not exist...Try again"
                form = Login()
                return render(request,"index.html",{'error':error})
            else:
                user1 = user.objects.get(email=email)
                pass1 = form.cleaned_data['passwd']
                pass2 = user1.passwd
                print(pass1, pass2)
                # verify = hashers.check_password(pass1,pass2)
                if pass1 == pass2:
                    request.session['email'] = email
                    request.session['islogin'] = True

                    data={
                            'email': form.cleaned_data['email'],
                            'passwd': form.cleaned_data['passwd']
                        }
                    return render(request,"afterlogin.html",{'data':data})
                else:
                    error = "Incorrect Password"
                    form = Login()
                    return render(request,'index.html',{'error':error,'form':form})
        else:
            error="method is not valid"
            form=Login()
            return render(request,"login.html",{"error":error,'form':form})
    else:
        error = "Form is not valid"
        form = Login()
        return render(request,"index.html",{'error':error,'form':form})

def logout(request):
    del request.session['islogin']
    del request.session['email']
    form = Login()
    return render(request,"index.html")

class signup(View):
    #return render(request,"signup.html")
    def get(self,request):
        error="method is not valid"
        form=Signup()
        return render(request,'index.html',{'form':form,'error':error})
    def post(self,request):
        form=Signup(request.POST,request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)
            try:
                u = user.objects.get(email=email)
            except user.DoesNotExist as e:
            #user=form.cleaned_data['Username']
            #Phone=form.cleaned_data['Phone'],
                pass1=form.cleaned_data['passwd']
                cpass=form.cleaned_data['cpasswd']
                if pass1==cpass:
                    
                    from_email = "sameersharma1904@gmail.com"
                    to_email = form.cleaned_data['email']
                    otp = str(randint(0000,9999))
                    subject="Message for email verification"
                    message = "Your otp for email verification is "+otp
                    try:
                        send_mail(subject,message,from_email,(to_email,),auth_password=settings.EMAIL_HOST_PASSWORD)
                    except:
                        error = "Invalid email..."
                        return render(request,"index.html",{'error':error})
                    else:
                        request.session['otp'] = otp
                        request.session['email'] = form.cleaned_data['email']
                        request.session['firstname'] = form.cleaned_data['firstname']
                        request.session['lastname'] = form.cleaned_data['lastname']
                        request.session['passwd'] = form.cleaned_data['passwd']
                        request.session['phone'] = form.cleaned_data['phone']
                        request.session['gender'] = form.cleaned_data['gender']
                        error = "Check email for otp"
                        return render(request,"eotp.html",{'error':error})
                else:
                    error = "Password does not match!!Try again"
                    form = Signup()
                    return render(request,"index.html",{'form':form,'error':error})
            else:
                error = "User already exist..."
                return render(request,"index.html",{'error':error})
        else:
            error = "Invalid form"
            form = Signup()
            return render(request,"index.html",{'form':form,'error':error})


# def signup(request):
#     return render(request,"signup.html")
def logout(request):
    del request.session['email']
    del request.session['islogin']
    return render(request,'index.html')

def forgot(request):
    form = Otp()
    return render(request,"forgot.html",{'form':form})

def otp(request):
    form = Otp(request.POST)
    if form.is_valid():
        to_email = form.cleaned_data['email']
        from_email = "sameersharma1904@gmail.com"
        otp = str(randint(1000,9999))
        request.session['otp'] = otp
        request.session['email'] = to_email
        subject = "mail for otp"
        message = "Enter this otp for password change " + otp
        send_mail(subject,message,from_email,(to_email,),auth_password=settings.EMAIL_HOST_PASSWORD)
        return render(request,"otp.html")
    else:
        error = "Invalid form"
        form = Otp()
        return render(request,"forgot.html",{'error':error,'form':form})

def checkotp(request):
    form = CheckOtp(request.POST)
    if form.is_valid():
        otp = form.cleaned_data['otp']
        otp1 = request.session['otp']
        if otp == otp1:
            form = changepassword()
            del request.session['otp']
            return render(request,"changepassword.html",{'form':form})
        else:
            error = "Otp does not match try again"
            form = Otp()
            return render(request,"forgot.html",{'form':form,'error':error})
    else:
        error = "form invalid"
        form = Otp()
        return render(request,"forgot.html",{'form':form,'error':error})   

def change(request):
    form = changepassword(request.POST)
    if form.is_valid():
        password = form.cleaned_data['password']
        cpassword = form.cleaned_data['confirm_password']
        if password == cpassword:
            try:
                u = request.session.get('email')
                u1 = user.objects.get(email=u)
            except user.DoesNotExist as e:
                error = "No such user"
                form = Otp()
                return render(request,'forgot.html',{'form':form,'error':error})
            else:
                u1.passwd = password
                del request.session['email']
                return render(request,"index.html")
        else:
            error = "Password does not match"
            form = Otp()
            return render(request,"forgot.html",{'error':error,'form':form})

def postpg(request):
    form = Roompost()
    return render(request,'post.html')

class postpg1(View):
    def get(self,request):
        error="method is not valid"
        form=Roompost()
        return render(request,'post.html',{'form':form,'error':error})
    def post(self,request):
        form=Roompost(request.POST,request.FILES)
        if form.is_valid():
        #print(form)
        #try:
                data={
                    'description' : form.cleaned_data['description'],
                    'area':form.cleaned_data['area'],
                    'zipcode':form.cleaned_data['zipcode'],
                    'rent': form.cleaned_data['rent'],
                    'facilities' : form.cleaned_data['facilities'],
                    'meals':form.cleaned_data['meals'],
                    'name' : form.cleaned_data['name'],
                    'contact' : form.cleaned_data['contact'],
                    'roompic' : form.cleaned_data['roompic']
                    }
                new_post = postmodel.objects.create(**data)
                new_post.save()
                error = "Successfully posted"
                return render(request,"afterlogin.html",{'error':error})
        else:
            return render(request,"afterlogin.html",{'error':error})
        #except Exception as e:
            #return HttpResponse(e)

def getpg(request):
    data = postmodel.objects.filter(area="raja park")
    pgs = []
    if data:
        for var in data:
            dic = {
                'description' : var.description,
                'area':var.area,
                'rent': var.rent,
                'facilities' : var.facilities,
                'meals':var.meals,
                'name' : var.name,
                'contact' : var.contact,
                'roompic' : var.roompic
            }
            pgs.append(dic)
        return render(request,"data.html",{'pgs':pgs})
    else:
        error = "No pgs avaiable"
        return render(request,"pgs.html")

def sendmsg(request):
    form = Contact(request.POST)
    if form.is_valid():
        from_email = "sameersharma1904@gmail.com"
        to_email = "sameersharma1904@gmail.com"
        message = form.cleaned_data['message']
        email = form.cleaned_data['email']
        name = form.cleaned_data['name']
        final_message = f"""name : {name}
        email : {email}
        message : {message}"""
        subject = "Message for query"
        send_mail(subject,final_message,from_email,(to_email,),auth_password=settings.EMAIL_HOST_PASSWORD) 
        error = "Message send successfully"
        return render(request,"index.html",{'error':error})
    else:
        error = "Invalid form"
        return render(request,"index.html",{'error':error}) 

def checkeotp(request):
    form = CheckOtp(request.POST)
    if form.is_valid():
        otp1 = form.cleaned_data['otp']
        otp2 = request.session['otp']
        if otp1 == otp2:
            # pwd = hashers.make_password(request.session.get('passwd'))
            data={
                    'email' : request.session['email'],
                    'firstname' : request.session['firstname'],
                    'lastname' : request.session['lastname'],
                    'passwd' : request.session['passwd'],
                    'phone' : request.session['phone'],
                    'gender' : request.session['gender'],
                }
            new_user = user.objects.create(**data)
            new_user.save()
            error = "User created..login to continue"
            del request.session['otp'] 
            del request.session['email'] 
            del request.session['firstname'] 
            del request.session['lastname'] 
            del request.session['passwd'] 
            del request.session['phone'] 
            del request.session['gender']
            #form = Login()
            return render(request,"index.html",{'error':error})
            #return redirect("/",{'error':error})
        else:
            error = "Otp does not match...try again"
            del request.session['otp'] 
            del request.session['email'] 
            del request.session['firstname'] 
            del request.session['lastname'] 
            del request.session['passwd'] 
            del request.session['phone'] 
            del request.session['gender']
            return redirect("/",{'error':error})


def getpg1(request):
    if request.session.get('email'):
        return render(request,"pgs.html")
    else:
        return redirect("/")


def getpg2(request):
    data = postmodel.objects.filter(area="gopalpura")
    pgs = []
    if data:
        for var in data:
            dic = {
                'description' : var.description,
                'area':var.area,
                'rent': var.rent,
                'facilities' : var.facilities,
                'meals':var.meals,
                'name' : var.name,
                'contact' : var.contact,
                'roompic' : var.roompic.url
            }
            pgs.append(dic)
        return render(request,"data.html",{'pgs':pgs})
    else:
        error = "No pgs avaiable"
        return render(request,"pgs.html",{'error':error})

def getpg3(request):
    data = postmodel.objects.filter(area="lal kothi")
    pgs = []
    if data:
        for var in data:
            dic = {
                'description' : var.description,
                'area':var.area,
                'rent': var.rent,
                'facilities' : var.facilities,
                'meals':var.meals,
                'name' : var.name,
                'contact' : var.contact,
                'roompic' : var.roompic.url
            }
            pgs.append(dic)
        return render(request,"data.html",{'pgs':pgs})
    else:
        error = "No pgs avaiable"
        return render(request,"pgs.html",{'error':error})

def getpg4(request):
    data = postmodel.objects.filter(area="malviya nagar")
    pgs = []
    if data:
        for var in data:
            dic = {
                'description' : var.description,
                'area':var.area,
                'rent': var.rent,
                'facilities' : var.facilities,
                'meals':var.meals,
                'name' : var.name,
                'contact' : var.contact,
                'roompic' : var.roompic.url
            }
            pgs.append(dic)
        return render(request,"data.html",{'pgs':pgs})
    else:
        error = "No pgs avaiable"
        return render(request,"pgs.html",{'error':error})

def getpg5(request):
    data = postmodel.objects.filter(area="jawahar nagar")
    pgs = []
    if data:
        for var in data:
            dic = {
                'description' : var.description,
                'area':var.area,
                'rent': var.rent,
                'facilities' : var.facilities,
                'meals':var.meals,
                'name' : var.name,
                'contact' : var.contact,
                'roompic' : var.roompic.url
            }
            pgs.append(dic)
        return render(request,"data.html",{'pgs':pgs})
    else:
        error = "No pgs avaiable"
        return render(request,"pgs.html",{'error':error})

def getpg6(request):
    data = postmodel.objects.filter(area="vaishali")
    pgs = []
    if data:
        for var in data:
            dic = {
                'description' : var.description,
                'area':var.area,
                'rent': var.rent,
                'facilities' : var.facilities,
                'meals':var.meals,
                'name' : var.name,
                'contact' : var.contact,
                'roompic' : var.roompic.url
            }
            pgs.append(dic)
            print(var.meals)
        return render(request,"data.html",{'pgs':pgs})
        
    else:
        error = "No pgs avaiable"
        return render(request,"pgs.html",{'error':error})

