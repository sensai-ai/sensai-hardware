import os

from supabase import Client, create_client
from supabase.client import ClientOptions

from server.services.utils import debug_print


class SupabaseClientManager:
    """Manages the Supabase client instance."""

    def __init__(self):
        self.supabase_config = {
            "supabase_url": os.getenv("SUPABASE_URL"),
            "supabase_key": os.getenv("SUPABASE_KEY"),
        }
        self.client: Client = create_client(
            **self.supabase_config,
            options=ClientOptions(
                postgrest_client_timeout=10,
                storage_client_timeout=10,
                schema="public",
            ),
        )

    def get_client(self) -> Client:
        """Returns the Supabase client instance."""
        debug_print(f"Supabase client: {self.client}")
        return self.client


if __name__ == "__main__":
    # test the supabase client
    SupabaseClientManager().get_client()
