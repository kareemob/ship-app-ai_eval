from pydantic import BaseModel, Field


class AgentToolCall(BaseModel):
    name: str
    args: dict
    result: str | None = None

class AgentResponse(BaseModel):
    reply: str
    tool_calls: list[AgentToolCall] = Field(alias="toolCalls")
    proposal: dict | None = None
    model: str
    latency_ms: int = Field(alias="latencyMs")    