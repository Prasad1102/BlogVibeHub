from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from Blogs.views import *

urlpatterns = [
    path('', home, name="Home"),
    path('register/', registerUser, name="registerUser"),
    path('createBlog/', createBlog, name="createBlog"),
    path('displayBlog/<uuid:id>/', displayBlog, name="displayBlog"),
    path('login/', loginUser, name="loginUser"),
    path('logout/', logoutUser, name="logoutUser"),
    path('testing/', testingRequirement, name="testingRequirement"),
    # _----------------------------FOLLOW USER _______________-------------------------------
    path('followUser/<int:id>/', followToUser, name="followToUser"),
    path('comment/<uuid:id>', commentToBlog, name="commentToBlog"),
    path('likeBlog/<uuid:id>', likeToBlog, name="likeToBlog"),
    # -------------------------PROFILE
    path('profile/<int:id>/', displayProfile, name="displayProfile"),
    path('about/', about, name="about"),
    # -----------------------Admin Url
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)