"""
Run:
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""
from typing import AsyncIterator

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from agents import Runner
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from chatkit.server import ChatKitServer, StreamingResult
from chatkit.types import ThreadMetadata, ThreadStreamEvent, UserMessageItem

from agents_rank_budget import router_agent
from chatkit_store import RankBudgetChatKitStore

load_dotenv()

app = FastAPI()


class RankBudgetChatKitServer(ChatKitServer[dict]):
    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: dict,
    ) -> AsyncIterator[ThreadStreamEvent]:
        # Load recent items then restore chronological order for model input.
        items = await self.store.load_thread_items(
            thread.id,
            after=None,
            limit=20,
            order="desc",
            context=context,
        )
        recent_items_in_order = list(reversed(items.data))
        input_items = await simple_to_agent_input(recent_items_in_order)

        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)
        result = Runner.run_streamed(
            starting_agent=router_agent,
            input=input_items,
            context=agent_context,
        )
        async for event in stream_agent_response(context=agent_context, result=result):
            yield event


store = RankBudgetChatKitStore()
server = RankBudgetChatKitServer(store=store)


@app.post("/chatkit")
async def chatkit(request: Request):
    result = await server.process(request=await request.body(), context={})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
