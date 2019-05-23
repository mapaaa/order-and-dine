from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    path('logout/', views.logout_view, name='logout'),
    path('restaurant/<int:pk>/', views.restaurant, name='restaurant'),
    path('<str:action>/', views.index2, name='index2'),
    path('reservation/<int:pk>', views.reservation, name='reservation')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
