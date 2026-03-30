from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()

Supabase_url = os.getenv("Supabase_url")
Supabase_key = os.getenv("Supabase_key")


supabase: Client = create_client(Supabase_url, Supabase_key)
