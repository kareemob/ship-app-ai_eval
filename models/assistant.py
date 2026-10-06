from pydantic import BaseModel, Field


class Source(BaseModel):
    n: int
    source: str
    heading: str
    score: float

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    model: str
    latency_ms: int = Field(alias="latencyMs")    


class Chunk(BaseModel):
    id: int
    source: str
    heading: str
    content: str
    score: float


class SearchResponse(BaseModel):
    query: str
    k: int
    min_score: float = Field(alias="minScore")
    indexed_chunks: int = Field(alias="indexedChunks")
    results: list[Chunk]        