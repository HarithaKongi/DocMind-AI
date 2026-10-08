import httpx

from app.core.config import settings
from app.schemas.chat import Citation, ChatRequest, ChatResponse
from app.schemas.retrieval import RetrievalRequest
from app.services.retrieval import retrieve

INSUFFICIENT_EVIDENCE = (
    "I couldn't find enough evidence in the selected documents to answer this question."
)

SYSTEM_PROMPT = """You are DocMind AI, a document-grounded knowledge assistant.
Answer questions using only the supplied document excerpts. Do not rely on outside knowledge.
If the excerpts do not contain enough evidence, say that you couldn't find enough evidence in the selected documents.
Never invent facts, citations, page numbers, or quotations.
Keep the answer concise and cite supporting excerpts using [Source 1], [Source 2], etc."""


class GenerationProvider:
    async def generate(self, question: str, context: str) -> str:
        raise NotImplementedError


class HostedGenerationProvider(GenerationProvider):
    def __init__(self) -> None:
        if not settings.llm_api_key:
            raise RuntimeError("LLM is not configured. Set LLM_API_KEY.")
        self.api_key = settings.llm_api_key
        self.api_url = settings.llm_api_url
        self.model = settings.llm_model

    async def generate(self, question: str, context: str) -> str:
        payload = {
            "model": self.model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Document excerpts:\n\n{context}\n\n"
                        f"Question: {question}"
                    ),
                },
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        try:
            answer = data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("The generation provider returned an invalid response.") from exc

        if not answer:
            raise RuntimeError("The generation provider returned an empty answer.")

        return answer


_generation_provider: GenerationProvider | None = None


def get_generation_provider() -> GenerationProvider:
    global _generation_provider
    if _generation_provider is None:
        _generation_provider = HostedGenerationProvider()
    return _generation_provider


def _build_context(results) -> str:
    sections = []
    for index, result in enumerate(results, start=1):
        sections.append(
            f"[Source {index}]\n"
            f"Document ID: {result.document_id}\n"
            f"Page: {result.page_number}\n"
            f"Similarity: {result.similarity:.4f}\n"
            f"Excerpt:\n{result.content}"
        )
    return "\n\n".join(sections)


def _build_citations(results) -> list[Citation]:
    return [
        Citation(
            document_id=result.document_id,
            page_number=result.page_number,
            excerpt=result.content,
        )
        for result in results
    ]


async def chat(access_token: str, request: ChatRequest) -> ChatResponse:
    retrieval_request = RetrievalRequest(
        query=request.question,
        document_ids=request.document_ids,
        top_k=request.top_k,
    )
    retrieval_response = await retrieve(
        access_token=access_token,
        request=retrieval_request,
    )

    if not retrieval_response.results:
        return ChatResponse(
            answer=INSUFFICIENT_EVIDENCE,
            grounded=False,
            citations=[],
        )

    context = _build_context(retrieval_response.results)
    answer = await get_generation_provider().generate(
        question=request.question,
        context=context,
    )

    return ChatResponse(
        answer=answer,
        grounded=True,
        citations=_build_citations(retrieval_response.results),
    )
