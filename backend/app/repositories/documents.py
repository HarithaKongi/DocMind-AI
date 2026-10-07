from app.core.supabase import get_supabase_client


class SupabaseDocumentRepository:
    async def create(
        self,
        user_id: str,
        filename: str,
        file_size: int,
        page_count: int,
    ) -> str:
        client = get_supabase_client()

        response = (
            client.table("documents")
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
        client = get_supabase_client()

        client.table("documents").update(
            {
                "status": status,
                "error_message": error_message,
            }
        ).eq("id", document_id).execute()
