from django.urls import path
from users import views
from users.views import UserLoginView, UserRegistrationView, UserProfileView, UserCartView

app_name = 'users'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration', UserRegistrationView.as_view(), name='registration'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('logout', views.logout, name='logout'),
    path('users-cart/', UserCartView.as_view(), name='users_cart'),

    path('users-list/', views.UsersList.as_view(), name='users_list'),
    path('users-retrieve/<str:username>/', views.UsersRetrieveUpdateDestroy.as_view(), name='users_retrieve_update_destroy'),
]