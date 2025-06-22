from supabase import create_client, Client

from utils.config import SUPABASE_ANON_KEY, SUPABASE_URL


supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
