import requests
from docs import documents


def search_top_k(query, documents, k=2):
    query_words = query.split()
    scored_docs = []

    for doc in documents:
        overlap_count = 0
        for word in query_words:
            word_stem = word[:-1] if len(word) > 2 else word
            if word in doc or word_stem in doc:
                overlap_count += 1

        scored_docs.append((overlap_count, doc))

    scored_docs.sort(reverse=True)

    top_docs = scored_docs[:k]

    return [doc for score, doc in top_docs]

def count_docs_with_word(word, documents):
    count = 0
    for doc in documents:
        if word in doc:
            count += 1
    return count


def search_final(query, documents, k=2):
    query_words = query.split()
    total_docs = len(documents)

    scores = []
    for doc in documents:
        doc_score = 0
        for word in query_words:
            word_stem = word[:-1] if len(word) > 2 else word

            matched_word = None
            if word in doc:
                matched_word = word
            elif word_stem in doc:
                matched_word = word_stem

            if matched_word:
                doc_count = count_docs_with_word(matched_word, documents)
                if doc_count > 0:
                    doc_score += total_docs / doc_count

        scores.append((doc_score, doc))

    scores.sort(reverse=True)
    top_docs = scores[:k]
    return [doc for score, doc in top_docs]

def ask_ollama(question, context):
    prompt = f"""아래 참고 문서를 보고 질문에 답해줘. 문서에 없는 내용이면 모른다고 답해줘.

[참고 문서]
{context}

[질문]
{question}"""

    payload = {
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return response.json()["response"]


# 실행 부분
if __name__ == "__main__":
    question = "별풍선 수수료는 얼마야?"
    found_docs = search_final(question, documents, k=2)

    print("검색된 문서들:")
    for d in found_docs:
        print(" -", d)
    print()

    context = "\n".join(found_docs)
    answer = ask_ollama(question, context)
    print("챗봇 답변:", answer)
