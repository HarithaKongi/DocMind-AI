from app.core.supabase import supabase_rest


class SupabaseDocumentRepository:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def create(self, user_id: str, filename: str, file_size: int, page_count: int) -> str:
        response = await supabase_rest(
            "POST", "/rest/v1/documents", self.access_token,
            json={"user_id": user_id, "filename": filename, "file_size": file_size,
                  "page_count": page_count, "status": "processing"},
            params={"select": "id"},
        )
        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Supabase returned a non-JSON response while creating the document "
                f"(status {response.status_code})."
            ) from exc

        if not data or not data[0].get("id"):
            raise RuntimeError("Supabase created no document row.")
        return str(data[0]["id"])

    async def update_status(self, document_id: str, status: str, error_message: str | None = None) -> None:
        await supabase_rest(
            "PATCH", "/rest/v1/documents", self.access_token,
            json={"status": status, "error_message": error_message},
            params={"id": f"eq.{document_id}"},
        )
