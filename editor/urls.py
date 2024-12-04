
from django.urls import path
from . import views

urlpatterns = [
    path('document/<int:doc_id>/', views.open_document, name='open_document'),
    path('document/new/', views.create_document, name='create_document'),
    path('document/<int:doc_id>/autosave/', views.autosave_document, name='autosave_document'),
    path('document/<int:doc_id>/download/', views.download_document, name='download_document'),
    path('', views.home, name='home'),
    path('editor/document/list/', views.list_documents, name='list_documents'),
    path('editor/document/<int:doc_id>/content/', views.load_document, name='load_document'),
    path('document/<int:doc_id>/add_comment/', views.add_comment, name='add_comment'),
    path('document/<int:doc_id>/comments/', views.get_comments, name='get_comments'),
    path("register/",views.register_view,name='register'),
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    

]

