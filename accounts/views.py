from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User,UserProfile
from seller.forms import SellerForm
from django.contrib import messages,auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
       messages.warning(request,'You are already Logged in!') 
       return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create user using custom create_user method
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'your accounts has been registered successfully!')
            print("User created successfully.")
            return redirect('registerUser')  # or redirect to 'login' or success page
        else:
            # If the form is invalid, show errors in the template
            print("Form invalid")
            print(form.errors)
            return render(request, 'accounts/registerUser.html', {'form': form})
    else:
        form = UserForm()
    
    return render(request, 'accounts/registerUser.html', {'form': form})

#restrict the user from accessesing the customer page
def check_role_seller(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
     
#restrict the user from accessesing the seller page

def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

def registerSeller(request):
    if request.user.is_authenticated:
       messages.warning(request,'You are already Logged in!') 
       return redirect('dashboard')
    elif request.method=='POST':
        #store the data and create the user
        form=UserForm(request.POST)
        s_form=SellerForm(request.POST,request.FILES)
        if form.is_valid() and s_form.is_valid:
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.SELLER
            user.save()
            seller=s_form.save(commit=False)
            seller.user=user
            user_profile=UserProfile.objects.get(user=user)
            seller.user_profile=user_profile
            seller.save()
            messages.success(request,'seller account has been successfully registred! please wait for the approval')
            return redirect('registerseller')
        else:
            print('invalid form')
            print(form.errors)
        
    else:
        form=UserForm()
        s_form=SellerForm()
    context={
        'form':form,
        's_form':s_form
    }
    return render(request,'accounts/registerSeller.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custdashboard(request):
    return render(request,'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_seller)
def sellerdashboard(request):
    return render(request,'accounts/sellerDashboard.html')