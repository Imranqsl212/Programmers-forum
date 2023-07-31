from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include

# def home(request):
#     return HttpResponse('home page')
# def about(request):
#     return HttpResponse('about page')
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', home),
#     path('about/', about)
# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]
