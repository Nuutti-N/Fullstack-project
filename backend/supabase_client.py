from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")


supabase: Client = create_client(supabase_url, supabase_key)
