from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import check_password
from django.contrib import messages

from myApp.models import *


def signupPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        displayname= request.POST.get('display_name')
        mail= request.POST.get('email')
        pass_word= request.POST.get('password')
        usertype= request.POST.get('user_type')
        user = Custom_User.objects.create_user(username=user_name,password=pass_word)
        user.display_name=displayname
        user.email=mail
        user.user_type=usertype
        user.save()
        return redirect("signinPage")

    return render(request,'signup.html')

def logoutPage(request):

    logout(request)

    return redirect('signinPage')

def signinPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=user_name, password=password)

        print(user)

        if user:
            login(request,user)
            return redirect("dashboardPage")


    return render(request,'login.html')

@login_required
def dashboardPage(request):

    return render(request,"dashboard.html")

@login_required
def viewjobPage(request):

    job=job_model.objects.all()

    context={
        'job':job
    }
    return render(request,"viewjob.html",context)

def add_job_Page(request):

    user = request.user

    if request.method == 'POST':

        jobTitle=request.POST.get('jobTitle')
        companyName=request.POST.get('companyName')
        location=request.POST.get('location')
        description=request.POST.get('description')

        job=job_model(
            job_title=jobTitle,
            company_name=companyName,
            location=location,
            description=description,
            job_creator=user,
        )
        job.save()

        return redirect("viewjobPage")
    

    return render(request,'Recruiter/Addjob.html')

def deletePage(request,myid):

    job=job_model.objects.filter(id=myid)
    job.delete()

    return redirect("viewjobPage")

def editPage(request,myid):

    job=job_model.objects.filter(id=myid)

    return render(request,'Recruiter/editJob.html',{'job':job})

def updatePage(request):

    user = request.user
    if request.method == 'POST':

        job_id=request.POST.get('jobid')
        jobTitle=request.POST.get('jobTitle')
        companyName=request.POST.get('companyName')
        location=request.POST.get('location')
        description=request.POST.get('description')
        job=job_model(
            id=job_id,
            job_title=jobTitle,
            company_name=companyName,
            location=location,
            description=description,
            job_creator=user,
        )
        job.save()
        return redirect("viewjobPage")


def applyPage(request,myid):

    job=job_model.objects.filter(id=myid)
    

    return render(request,'JobSeeker/applyjob.html')


def ProfilePage(request):
    
    user=request.user
    
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)


@login_required
def EditProfilePage(request):
    if request.method == 'POST':
        user = request.user

        # Check if the entered password matches the user's current password
        entered_password = request.POST['password']
        if not check_password(entered_password, user.password):
            messages.error(request, 'Incorrect password. Profile not updated.')
            return redirect('EditProfilePage')

        # Continue with profile update
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.display_name = request.POST['display_name']
        user.skills = request.POST['skills']
        
        profile_picture=request.FILES.get('image')
        print(profile_picture)

        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('ProfilePage')  # Redirect to the profile page after successful update
    
    return render(request, 'Editprofile.html')





    