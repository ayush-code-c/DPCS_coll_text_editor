# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Document
from io import BytesIO
from docx import Document as WordDocument

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
    if request.method == 'POST':
        doc = get_object_or_404(Document, id=doc_id)
        content = request.POST.get('content', '')
        doc.content = content
        doc.save()
        return JsonResponse({'status': 'success', 'message': 'Document autosaved.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# Download document in Word format
def download_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    word_doc = WordDocument()
    word_doc.add_heading(doc.title, level=1)
    word_doc.add_paragraph(doc.content)

    # Save the Word document to a BytesIO buffer
    buffer = BytesIO()
    word_doc.save(buffer)
    buffer.seek(0)

    # Serve the Word document as a response
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{doc.title}.docx"'
    return response

def home(request):
    documents = Document.objects.all()
    return render(request, 'editor/home.html', {'documents': documents})

