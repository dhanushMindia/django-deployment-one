# core/urls.py
from django.contrib import admin
from django.urls import path, include


from users.views import GoogleLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your existing app URLs
    path('api/', include('api.urls')),
    path('api/users/', include('users.urls')),

    # --- New, explicit authentication URLs ---
    
    # URLs for dj-rest-auth's standard features (logout, etc.)
    path('api/auth/', include('dj_rest_auth.urls')),
    
    # URL for our custom Google Login view
    path('api/auth/google/', GoogleLoginView.as_view(), name='google_login'),
    
    # URLs for Simple JWT (email/password login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
