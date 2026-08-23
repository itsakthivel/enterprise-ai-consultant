from app.rag.document_loader import load_document


def test_load_document():
    document = load_document("sample_docs/architecture.md")

    assert document.filename == "architecture.md"
    assert document.source == "sample_docs"
    assert document.content
