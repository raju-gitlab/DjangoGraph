from django.contrib import admin
from django.urls import path, include
from analysisapp import views

urlpatterns = [
    path("", views.index, name='home'),
    path("login", views.login, name='login'),
    path("register", views.register, name='register'),
    path("home", views.homepage, name='homepage'),
    path("upload", views.upload, name='upload'),
    path("uploadfile", views.uploaddatafiles, name='uploaddatafiles'),
    path("uploaddata", views.uploaddata, name='uploaddata'),
    path("managedata", views.managedata, name='managedata'),
    path(r"deletefiles/", views.deletedataset, name='deletedataset'),
    # path(r"analyze/", views.makegraph, name='makegraph')
    path(r"analyze/", views.makegraph, name='makegraph'),
    path(r"graph/", views.checkuploads, name='checkuploads'),
    path(r"removecolumns/", views.removecolumns, name='removecolumns'),
    # path("removeduplicates" , )
]
