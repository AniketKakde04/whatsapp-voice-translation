import os
from supabase import create_client, Client
from security_utils import encrypt_text

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_sensitive_data():
    result = supabase.table("sensitive_info").select("*").execute()
    rows = result.data or []
    return {row['original']: row['encrypted'] for row in rows}

def add_sensitive_item(text):
    print(f"[SUPABASE] Trying to store: {text}")
    
    existing = supabase.table("sensitive_info").select("id").eq("original", text).execute()
    if existing.data:
        print(f"[SUPABASE] Already exists: {text}")
        encrypted_row = supabase.table("sensitive_info").select("encrypted").eq("original", text).execute()
        return encrypted_row.data[0]["encrypted"]

    encrypted = encrypt_text(text)

    # Insert and check result
    insert_response = supabase.table("sensitive_info").insert({
        "original": text,
        "encrypted": encrypted
    }).execute()

    if insert_response.status_code >= 400:
        print(f"[SUPABASE] Insert failed: {insert_response.status_code} - {insert_response.data}")
    else:
        print(f"[SUPABASE] Inserted: {text}")

    return encrypted
