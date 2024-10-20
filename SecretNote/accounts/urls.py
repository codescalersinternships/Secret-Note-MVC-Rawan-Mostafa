from django.urls import path
from django_ratelimit.decorators import ratelimit
from .views import SignUpView


urlpatterns = [
    path("signup/", ratelimit(key='ip', rate='20/m', method='POST', block=True) (SignUpView.as_view()), name="signup"),

]