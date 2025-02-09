"""
URL configuration for StoryPanda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.users.api.v1.endpoints import router as user_router
from apps.auth.api.v1.endpoints import auth_router

api = NinjaAPI(
    title="StoryPanda API", version="1.0.0", description="StoryPanda API documentation"
)

# Add routers - note the path format
api.add_router("/v1/users/", user_router, tags=["Users"])
api.add_router("/v1/auth/", auth_router, tags=["Auth"])

urlpatterns = [path("admin/", admin.site.urls), path("api/", api.urls)]
