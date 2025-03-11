from django.urls import path

from router.views import index

urlpatterns = [
    path('', index)
]