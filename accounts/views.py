from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

def registerUser(request):
    if request.method == 'POST':
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
