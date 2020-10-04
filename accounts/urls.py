from django.urls import path
from accounts.views import \
    SubmittableLoginView, SubmittablePasswordChangeView, SuccessMessagedLogoutView, SignUpView, IndexView

app_name = 'accounts'
urlpatterns = [
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('passwordchange/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('logout/', SuccessMessagedLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', IndexView, name='index'),
]
