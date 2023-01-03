"""codetest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django import views as dviews
from django.conf import settings
from myapp import views
from .swagger import schema_view

urlpatterns = [
    url(r"^$", views.frontpage),
    url(r"^docs$", schema_view),
    path("admin/", admin.site.urls),
    path("api/v1/comment", views.CommentListView.as_view(), name="comments_list",),
    path(
        "api/v1/comment/<int:pk>",
        views.CommentDetailView.as_view(),
        name="comment_detail",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        url(
            r"^static/(?P<path>.*)$",
            dviews.static.serve,
            {"document_root": settings.STATIC_ROOT},
        ),
    ]
