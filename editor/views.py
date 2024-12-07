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
#from .middlewares import auth, guest
from .db_utils import save_document_to_db
from .db_utils import fetch_document_from_db

def save_document(request, doc_id):
    if request.method == "POST":
        data = request.POST  # Or `json.loads(request.body)` if using JSON
        content = data.get('content', '')  # Editor content
        comments = data.get('comments', [])  # Comments as JSON array
        save_document_to_db(doc_id, content, comments)
        return JsonResponse({"message": "Document saved successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)


#@guest
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


def add_comment(request, doc_id):
    if request.method == 'POST':
        document = get_object_or_404(Document, id=doc_id)
        data = json.loads(request.body)
        comment = Comment.objects.create(
            document=document,
            user=request.user,
            content=data['content'],
            start=data['start'],
            end=data['end']
        )
        return JsonResponse({'status': 'success', 'message': 'Comment added', 'comment_id': comment.id})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_comments(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    comments = document.comments.values('id', 'content', 'start', 'end', 'user__username', 'created_at')
    return JsonResponse({'status': 'success', 'comments': list(comments)})





def open_document(request, doc_id):
    document = fetch_document_from_db(doc_id)
    if document:
        return JsonResponse({"document": document})
    return JsonResponse({"error": "Document not found"}, status=404)

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

