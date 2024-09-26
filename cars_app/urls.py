from django.urls import path
from .views import register, user_login, user_logout, home, profile_view,place_order,car_detail,add_comment  
from .views import update_profile 
from .views import change_password

urlpatterns = [
    path('', home, name='home'), 
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('change-password/', change_password, name='change_password'),
    path('order/<int:car_id>/', place_order, name='place_order'),
    path('car/<int:car_id>/', car_detail, name='car_detail'), 
    path('car/<int:car_id>/comment/', add_comment, name='add_comment'),
]


