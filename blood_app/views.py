from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserExtend,RequestBlood,District,BloodGroup
from .forms import UserForm1, UserForm2, LoginForm, RequestForm, ChangeForm1, ChangeForm2
from django.db.models import Count
from django.contrib.auth.forms import PasswordChangeForm


def homepage(request):
    all_group = BloodGroup.objects.annotate(total=Count('userextend'))
    return render(request, "blood_app/home.html",{"all_group":all_group})



def registerView(request):
    if request.method == "POST":
        form1 = UserForm1(request.POST)
        form2 = UserForm2(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            obj = form1.save(commit=False)
            obj.set_password(obj.password)
            obj.save()
            obj2 = form2.save(commit=False)
            obj2.donor = obj
            obj2.save()
            return redirect('login')
    else:
        form1 = UserForm1()
        form2 = UserForm2()

    return render(request, "blood_app/register.html", {'form1':form1,'form2':form2})


def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    return render(request, "blood_app/login.html", {'form':form})


def logoutView(request):
    logout(request)
    return redirect('home')

@login_required
def profileView(request):
    return render(request, "blood_app/profile.html")


def createReqView(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allrequest')
    else:
        form = RequestForm()

    return render(request, "blood_app/brequest.html", {'form':form})


def allReqView(request):
    all_req = RequestBlood.objects.all()
    return render(request, "blood_app/allrequest.html", {'all_req':all_req})



def groupView(request, id):
    obj = get_object_or_404(BloodGroup, pk=id)
    donor = UserExtend.objects.filter(blood_group=obj)
    return render(request, "blood_app/donorlist.html", {'donor':donor})


def detailView(request, id):
    obj = get_object_or_404(User, pk=id)
    return render(request, "blood_app/details.html", {'obj':obj})

@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "blood_app/password.html", {'form':form})


@login_required
def editProfileView(request):
    if request.method == "POST":
        form1 = ChangeForm1(request.POST, instance=request.user)
        form2 = ChangeForm2(request.POST,request.FILES, instance=request.user.userextend)
        if form1.is_valid() and form2.is_valid():
            obj = form1.save()
            obj2 = form2.save(commit=False)
            obj2.donor = obj
            obj2.save()
            return redirect('profile')
    else:
        form1 = ChangeForm1(instance=request.user)
        form2 = ChangeForm2(instance=request.user.userextend)
    return render(request, "blood_app/edit_profile.html", {'form1':form1,'form2':form2})


@login_required
def statusView(request):
    obj = request.user.userextend
    if obj.ready_to_donate:
        obj.ready_to_donate = False
        obj.save()
    else:
        obj.ready_to_donate = True
        obj.save()
    return redirect('profile')


def getRequestView(request):
    if request.method == "POST":
        pin = request.POST.get("pin")
        obj = get_object_or_404(RequestBlood, pin_code=int(pin))
        return render(request, "blood_app/get_request.html",{'obj':obj})

    return render(request, "blood_app/get_request.html")

def editRequestView(request, pin):
    obj = get_object_or_404(RequestBlood, pin_code=pin)
    if request.method == "POST":
        form = RequestForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('allrequest')
    else:
        form = RequestForm(instance=obj)

    return render(request, "blood_app/edit_request.html",{'form':form})

def deleteRequestView(request, pin):
    obj = get_object_or_404(RequestBlood, pin_code=pin)
    obj.delete()
    return redirect('allrequest')
