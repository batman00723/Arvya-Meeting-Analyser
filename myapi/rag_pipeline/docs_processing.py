from myapi.models import Document, DocumentChunk
from myapi.rag_pipeline.ragpipeline import RagPipeline 
from myapi.rag_pipeline.docs_parsing import extract_content
from django.contrib.postgres.search import SearchVector

def document_processing(doc_id):
    try:
        document= Document.objects.get(id= doc_id)
        # Parse the content
        text= extract_content(document.document.path, document.file_type)

        if text:
            # Get Parsed content from DB
            document.raw_content= text
            document.save()

            pipeline= RagPipeline()

            # Process the Document into ingestion Pipeline
            chunk_count= pipeline.process_document(document, text)

            # Create vectors of chunks
            DocumentChunk.objects.filter(document_id= doc_id).update(
                search_vector= SearchVector('chunk')
            )
            document.status= "COMPLETED"
            document.save()

        else:
            document.status= "FAILED"
            print("Failed to Process Document")
            return f"Can't process document of doc_id {doc_id}"
        
    except Document.DoesNotExist:
        return f"Document of doc_id {doc_id} is not found"