import requests

url = "http://localhost:11434/api/generate"

for i in range(5):
    payload = {
    "model": "qwen2.5:7b",
    "prompt": "나랑 이야기 할 때는 한국어만 써줄래?",
    "stream": False
    }

    response = requests.post(url, json=payload)

    print(f"요청 {i+1}번:")
    print("상태 코드:", response.status_code)
    print("응답 내용:", response.json()["response"])
    print()