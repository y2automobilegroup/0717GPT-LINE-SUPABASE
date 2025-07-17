
from supabase import create_client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def query_supabase(gpt_vector):
    response = supabase.rpc("match_car_data", {
        "query_embedding": gpt_vector,
        "match_threshold": 0.80,
        "match_count": 1
    }).execute()

    if response.data and len(response.data) > 0:
        return response.data[0]['text']
    return None
