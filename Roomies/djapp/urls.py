from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index),
    path('sign_in/',views.signin,name='sign_in'),
    path('signup/',views.signup,name='signup'),
    path('profile/',views.profile.as_view(),name='profile'),
    path('log_out/<int:qk>/',views.log_out,name='log_out'),
    path('menu/',views.menu),
    path('product/',views.all_product,name="product"),
    path('add_product/',views.data,name='add_product'),
    path('delete/<int:qk>/',views.delete_data),
    path("profile/<name>/",views.all_profile,name="myprofile"),
    path('album/',views.album,name='album'),
    path('newalbum/',views.newalbum,name='newalbum')
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
