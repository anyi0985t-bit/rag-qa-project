import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="module")
def api_context():
    with sync_playwright() as p:
        context = p.request.new_context(base_url=BASE_URL)
        yield context
        context.dispose()


def test_정상질문은_200과_답변을_반환한다(api_context):
    response = api_context.post("/chat?question=별풍선 수수료는 얼마야?")
    assert response.status == 200
    body = response.json()
    assert len(body["answer"]) > 0
    assert isinstance(body["sources"], list)


def test_빈질문은_400을_반환한다(api_context):
    response = api_context.post("/chat?question=")
    assert response.status == 400


def test_공백질문은_400을_반환한다(api_context):
    response = api_context.post("/chat?question=   ")
    assert response.status == 400


def test_문서에없는질문도_정상응답한다(api_context):
    response = api_context.post("/chat?question=별풍선 창시자가 누구야?")
    assert response.status == 200
    assert len(response.json()["answer"]) > 0


def test_응답시간이_30초이내다(api_context):
    import time
    start = time.time()
    response = api_context.post("/chat?question=VOD 보관 기간 알려줘")
    elapsed = time.time() - start
    assert response.status == 200
    assert elapsed < 30, f"응답 시간 초과: {elapsed:.1f}초"