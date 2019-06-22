from django.urls import path

from qa_tools.views import create_test_user


urlpatterns = [
    path('create_test_user/', create_test_user, name='create_test_user'),
]
