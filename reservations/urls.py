from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('activate/<uuid:token>/', views.activate_account, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('find_bus/', views.find_bus, name='find_bus'),
    path('search_results/', views.search_results, name='search_results'),
    path('select_seats/<int:bus_id>/<str:date>/', views.select_seats, name='select_seats'),
    path('booking_confirmation/<int:bus_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('confirmation/<int:booking_id>/', views.confirmation, name='confirmation'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('help/', views.help_view, name='help'),
]

