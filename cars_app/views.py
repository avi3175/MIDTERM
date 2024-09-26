from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Order 
from .forms import UserUpdateForm ,CommentForm 

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages



from django.shortcuts import get_object_or_404
from .models import Car, Order,Brand






def home(request):
    brands = Brand.objects.all()
    cars = Car.objects.all()
    brand_filter = request.GET.get('brand')
    if brand_filter:
        cars = cars.filter(brand__name=brand_filter)

    return render(request, 'home.html', {'cars': cars, 'brands': brands})



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserRegistrationForm()
    return render(request, 'cars_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'cars_app/login.html', {'form': form})





@login_required
def profile_view(request):
    user_orders = Order.objects.filter(user=request.user).select_related('car')
    
    purchased_cars = {}

    for order in user_orders:
        car = order.car
        if car.id not in purchased_cars:
            purchased_cars[car.id] = {'count': 0, 'car': car}
        
        purchased_cars[car.id]['count'] += 1

    return render(request, 'cars_app/profile.html', {'orders': user_orders, 'purchased_cars': purchased_cars})




# Logout View
def user_logout(request):
    logout(request)
    return redirect('home') 



# user Update Form
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = UserUpdateForm(instance=request.user) 

    return render(request, 'cars_app/update_profile.html', {'form': form})



# Password Change

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'cars_app/change_password.html', {'form': form})





# Purchase or Placing Order

@login_required
def place_order(request, car_id):
    car = Car.objects.filter(id=car_id).first()  
    
    if not car:
        return render(request, 'cars_app/error.html', {'message': 'Car not found.'})  

  
    if car.quantity > 0:
        
        Order.objects.create(user=request.user, car=car)
        car.quantity -= 1
        car.save()
        
        messages.success(request, 'Order placed successfully!')
    else:
        messages.error(request, 'Sorry, this car is out of stock.')
    
    return redirect('home')  







# Car Details:

def car_detail(request, car_id):
    car = Car.objects.filter(id=car_id).first() 

    if not car:
        return render(request, 'car_not_found.html') 

    return render(request, 'cars_app/car_detail.html', {'car': car})



# Comments
@login_required
def add_comment(request, car_id):
    car = Car.objects.filter(id=car_id).first()  

    if not car:
        return render(request, 'cars_app/error.html', {'message': 'Car not found.'})  

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car  
            comment.name = request.user.username  
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('car_detail', car_id=car.id) 
    else:
        form = CommentForm()

    return render(request, 'cars_app/car_detail.html', {'car': car, 'form': form})
