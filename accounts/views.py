from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile
from django.contrib.auth import authenticate, login,logout
from .forms import SignupForm, UserForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def UserProfile(request):
    profile = get_object_or_404(Profile,user=request.user)
    posts = profile.favorite_posts.all()
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
   
    return render(request,'profile.html',{'profile':profile,"posts":posts,'user_form':user_form,'profile_form':profile_form})

# def UserLogin(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request,username=username,password=password)
#     if user is not None:
#         login(request,user)
#         return redirect ('index')
#     return render(request,'login.html')



def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')  # or any dashboard/main page
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def UserSignup(request):
    if request.method == 'GET':
        form = SignupForm()
        return render(request,'signup.html',{'form':form})
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
        
            
        return render(request,'signup.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')   
    
