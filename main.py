import google.generativeai as genai
from pydantic import BaseModel
key = ""
prompt = "以下の会話から、現在の話題を単語として出力してください。会話が複数の話題と関連している場合、それらすべてをリストとして出力してください。「あしたのバトラの配信楽しみだな。早くマリオパーティー人生縛りの続きが見たいわ。」"

class Topic(BaseModel):
    topic: list[str]

genai.configure(api_key=key)
gemini_pro = genai.GenerativeModel("gemini-2.0-flash")
response =  gemini_pro.generate_content(
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Topic],
    },
)
# Use the response as a JSON string.
print(response.text)

# Use instantiated objects.
topics : list[Topic] = response.parsed
print(topics)