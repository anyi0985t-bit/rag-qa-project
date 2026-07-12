from docs import documents

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

results = search_final("별풍선 수수료는 얼마야?", documents, k=2)
print("질문: 별풍선 수수료는 얼마야?")
for d in results:
    print(" -", d[:40])