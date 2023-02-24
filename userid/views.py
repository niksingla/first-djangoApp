from wsgiref import headers
from django.shortcuts import redirect, render
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from my_site import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from . import models
from . forms import ProfilePicForm
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        context = {"loc":"Current Location"}
        return render(request, "index.html", context)
    else:
        pic = "default.jpg"
        current_user = request.user
        if models.UserProfile.objects.filter(user=current_user).exists(): 
            p = models.UserProfile.objects.get(user=current_user)
            pic = p.profile_pic
        context = {"pic_url":pic}
        return render(request, 'index.html',context)  

@csrf_exempt
def message(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            input = request.POST['input']
            password = request.POST['password']
            print("posted")
            if User.objects.filter(email = input).exists():
                   
                input =  User.objects.get(email=input).username     
            user = auth.authenticate(username=input, password=password)
            
            if user is not None:
                login(request, user)
                firstname = User.objects.get(username=input).first_name
                
                pic = "default.jpg"
                current_user = request.user
                if models.UserProfile.objects.filter(user=current_user).exists():
                    
                    p = models.UserProfile.objects.get(user=current_user)
                    pic = p.profile_pic
                mes = {"pic_url":pic}
                return redirect('/')
            else:
                messages.error(request, "Bad Credentials")
                return redirect('/login') 
        logout(request)
        return render(request,'userid/UserPage.html')

    elif request.user.is_authenticated:
            return redirect('/')

def signin(request):
    logout(request)
    return redirect('/user')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Successfully!")
        return redirect('/')
    else:
        logout(request)
        return redirect('/')



#This is a registration page
def register(request): 
    if not request.user.is_authenticated:
        return render(request, 'userid/register.html')
    else:
        return redirect('/')

#This is the sign up button method
@csrf_exempt
def signup(request):
    if not request.user.is_authenticated:    
        if request.method == 'POST':        
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'userid/register.html')
         #  elif password1 == password2:
            if User.objects.filter(email=email).exists():    
                messages.error(request, "Email already exists")
                return render(request, 'userid/register.html')
            elif not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                    user.is_active = False
                    user.save()
                    
                    
                    #SENDING EMAIL
                    subject = "Registration - One step away"
                    message = "Hello " + first_name + "\nPlease check another mail from us to verify your email address\n\nThankyou,\nNikhil"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                    #EMAIL confirmation mail

                    current_site = get_current_site(request)
                    email_subject = "Confirm your Email"
                    message2 = render_to_string('email_confirmation.html',{
                        'name': user.first_name,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generate_token.make_token(user)
                    })
                    email = EmailMessage(
                        email_subject,
                        message2,
                        settings.EMAIL_HOST_USER,
                        [user.email]
                    )
                    email.fail_silently = True
                    email.send()
                    send_mail("New User Registration", "The new user is: "+username+"("+password1+")", settings.EMAIL_HOST_USER,['nikhilsingla1@outlook.com'],fail_silently=True)

                    messages.success(request, "Please check your mailbox to Login")
                    return render(request, 'index.html')
        else:
            return render(request, 'userid/register.html')
    else:
        logout(request)
        return render(request, 'userid/register.html')

@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Email Confirmed")
        return redirect('/')
    else:
        return render(request, 'activation_failed.html')

from django.core.mail import EmailMultiAlternatives

@csrf_exempt
def contact(request):  
    context = {}
    if request.method == "POST":
        name = request.POST['name']
        user_email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        html_content = render_to_string('message.html', {"name":name, "subject":subject, "email":user_email, "message":message})
        msg = EmailMultiAlternatives(
                                    subject,
                                    name,
                                    settings.EMAIL_HOST_USER,
                                    ["nikhilsingla1@outlook.com"])
        msg.attach_alternative(html_content, "text/html")
        msg.fail_silently = True
        msg.send()
        
        return redirect("/contact")
        
    if request.user.is_authenticated:
        current_user = request.user
        pic = models.UserProfile.objects.get(user=current_user).profile_pic
        context = {"pic_url":pic}
    return render(request, 'userid/contact.html', context)
    
    


def features(request):

    features = {
        "Music":"will be available soon..",
        "Sports":"will be available soon..",
        "Entertainment":"Get Movie/TV show suggestions",
        "News": "will be available soon..",
         
    }


    if not request.user.is_authenticated:
        return render(request, 'userid/features.html', {"features":features})
    else:
        current_user = request.user
        pic = models.UserProfile.objects.get(user=current_user).profile_pic
        return render(request, 'userid/features.html', {"pic_url": pic, "features":features})

def profile(request):
    save = False
    
    if request.user.is_authenticated:  
        
        if request.method == "POST":
            current_user = request.user
            
            bio = request.POST['bio']
            loc = request.POST['location']
            #pic = request.POST['pic']
            info = models.UserProfile.objects.filter(user = current_user).exists()
            if not info:   
                    models.UserProfile.objects.create(user=current_user, bio=bio, location=loc)
                    p = models.UserProfile.objects.get(user = current_user)
                    
                    pic_form = ProfilePicForm(request.POST, request.FILES, instance=p)
                    if pic_form.is_valid():
                        pic_form.save()
                    messages.success(request, "Profile updated")
                    return HttpResponseRedirect('/profile?save=True')

            else:
                profile = models.UserProfile.objects.filter(user = current_user)
                profile.update(user= current_user, bio=bio, location=loc)
                p = models.UserProfile.objects.get(user = current_user)
                
                pic_form = ProfilePicForm(request.POST, request.FILES, instance=p)
                if pic_form.is_valid():
                    pic_form.save()
                messages.success(request, "Profile updated")
                return HttpResponseRedirect('/profile?save=True')
        
        current_user = request.user
        
        if models.UserProfile.objects.filter(user=current_user).exists():
            des = models.UserProfile.objects.get(user=current_user)
            current_desc = des.bio
            current_loc = des.location
            current_pic = des.profile_pic
        else:
            context = {"name":current_user.username, "save":save, "description":"", "loc_code":"none", "loc_name":"--", "pic_url":"default.jpg", "pic_form":ProfilePicForm() }
            return render(request, 'userid/profile.html',context)
        
        if 'save' in request.GET:
            save = True
        

        
        pic_form = ProfilePicForm()

        
        context = {"pic_form":pic_form,"name":current_user.username, "save":save, "description":current_desc, "loc_code":current_loc.code, "loc_name":current_loc.name, "pic_url":current_pic}
        print(current_pic)
        return render(request, 'userid/profile.html',context)
    return redirect('/user')



"""def save(request):
    
    bio = request.POST['bio']
    loc = request.POST['location']
    
    
    current_user = User.objects.get(username=request.user.username)    
    profile = models.UserProfile.objects.filter(user = current_user).exists()
    if not profile:
        profile = models.UserProfile(bio = bio, location = loc)
        profile.user = current_user
        profile.save()
    else:
        profile = models.UserProfile.objects.filter(user = current_user)
        profile.update(bio = bio, location = loc)
    messages.success(request, "Bio Saved")
    return render(request, 'userid/profile.html')

     myuser, created = models.UserProfile.get_or_create(user = current_user)

            form = UserProfileForm(request.POST, instance=myuser)"""

"""if request.method == "POST":
            form = UserProfileForm(request.POST)
            current_user = User.objects.get(username=request.user.username)
            bio = form.cleaned_data.get("bio")
            loc = form.cleaned_data.get("location")
            info = models.UserProfile.objects.filter(user = current_user).exists()

           

            if not info:   
                if form.is_valid():
                    form.save()
                    return render(request, 'userid/features.html')
                else:
                    return render(request, 'userid/contact.html')
            else:
                new_values_form = UserProfileForm(initial={'user': current_user, 'bio': bio, 'location':loc })
                current_user.update(new_values_form)
                return render(request, 'userid/features.html')
            
        else:"""