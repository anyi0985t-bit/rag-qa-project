from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_빈질문은_400을_반환한다():
    response = client.post("/chat?question=")
    assert response.status_code == 400


def test_공백질문은_400을_반환한다():
    response = client.post("/chat?question=   ")
    assert response.status_code == 400


def test_검색함수가_정답문서를_찾는다():
    from rag_bot import search_final
    from docs import documents

    results = search_final("별풍선 수수료는 얼마야?", documents, k=2)
    combined = " ".join(results)
    assert "40%" in combined