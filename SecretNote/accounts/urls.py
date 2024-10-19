from django.urls import path
from django_ratelimit.decorators import ratelimit
from .views import SignUpView


urlpatterns = [
    path("signup/", ratelimit(key='ip', rate='5/m', method='POST', block=True) (SignUpView.as_view()), name="signup"),
    # path("signup/", SignUpView.as_view(), name="signup"),

]