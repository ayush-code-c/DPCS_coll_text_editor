# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Document
from io import BytesIO
from docx import Document as WordDocument
import json
from .models import Comment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout


new_doc = Document.objects.create(title="New Document")
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('open_document', doc_id=new_doc.id)
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html',{'form':form})

#@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('open_document', doc_id=new_doc.id)
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html',{'form':form}) 



def logout_view(request):
    logout(request)
    return redirect('login')




# Open an existing document
def open_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    return render(request, 'editor/document.html', {'doc_id': doc.id, 'title': doc.title, 'content': doc.content})

# Create a new document
def create_document(request):
    new_doc = Document.objects.create(title="New Document")
    return redirect('open_document', doc_id=new_doc.id)

# Autosave document content
def autosave_document(request, doc_id):
    if request.method == "POST":
        content = request.POST.get('content')  # Get content from the request
        doc = Document.objects.get(id=doc_id)
        doc.content = content  # Assuming the content field is a text field or JSON field
        doc.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

# Download document in Word format
def download_document(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
        content = doc.content
        word_doc = WordDocument()
        word_doc.add_paragraph(content)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="document.docx"'
        word_doc.save(response)
        return response
    except Document.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Document not found'}, status=404)

def home(request):
    documents = Document.objects.all()
    return render(request, 'editor/home.html', {'documents': documents})


def list_documents(request):
    documents = Document.objects.all()
    return JsonResponse({'status': 'success', 'documents': [doc.title for doc in documents]})


def load_document(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
        content = doc.content
        return JsonResponse({'status': 'success', 'content': content})
    except Document.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Document not found'}, status=404)

def rename_document(request, doc_id):
    if request.method == "POST":
        new_title = request.POST.get("new_title")
        try:
            document = Document.objects.get(id=doc_id)
            document.title = new_title
            document.save()
            return JsonResponse({"status": "success", "new_title": new_title})
        except Document.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Document not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
