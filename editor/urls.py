
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

]
