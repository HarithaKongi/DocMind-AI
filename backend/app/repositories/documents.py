from supabase import Client

from app.core.supabase import get_user_supabase_client


class SupabaseDocumentRepository:
    def __init__(self, access_token: str) -> None:
        self.client: Client = get_user_supabase_client(access_token)

    async def create(
        self,
        user_id: str,
        filename: str,
        file_size: int,
        page_count: int,
    ) -> str:
        response = (
            self.client.table("documents")
            .insert(
                {
                    "user_id": user_id,
                    "filename": filename,
                    "file_size": file_size,
                    "page_count": page_count,
                    "status": "processing",
                }
            )
            .select("id")
            .single()
            .execute()
        )

        return str(response.data["id"])

    async def update_status(
        self,
        document_id: str,
        status: str,
        error_message: str | None = None,
    ) -> None:
        self.client.table("documents").update(
            {
                "status": status,
                "error_message": error_message,
            }
        ).eq("id", document_id).execute()
