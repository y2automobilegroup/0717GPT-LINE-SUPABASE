
import openai

def process_message(message_text):
    system_prompt = "你是亞鈺汽車的客服助理，請根據問題判斷主題、品牌、年份，回傳一段查詢描述。"
    user_input = f"客戶問：{message_text}，請回傳查詢重點"

    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    query_text = res['choices'][0]['message']['content']

    emb_res = openai.Embedding.create(input=query_text, model="text-embedding-3-small")
    return emb_res['data'][0]['embedding']
