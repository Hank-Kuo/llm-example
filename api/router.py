from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Body

from langchain_core.exceptions import OutputParserException
from langfuse.decorators import langfuse_context, observe
from pydantic import BaseModel, Field


class RequestBody(BaseModel):
    question: str
    user_id: str


class ResponseBody(BaseModel):
    answer: str
  


router = APIRouter()


# summary_workflow = build_summary_workflow()
# translate_workflow = build_translate_workflow()

def get_uuid(request: RequestBody) -> str:
    return request.uuid


@router.get("/health")
async def health():
    return {"message": "OK"}


@router.post(
    "/api/v1/answer",
    response_model=ResponseBody,
    tags=["Answer"],
    summary="Answer your question",
    description="Answer your qeustion using OpenAI model",
    response_description="Summarized content and metadata",
)
@observe(capture_input=False)
async def questionAPI(
    request: RequestBody = Body(..., description="Request body containing the question"),
    langfuse_observation_id: str = Depends(get_uuid),
) -> ResponseBody:
    langfuse_context.update_current_trace(
        user_id=request.user_id,
        metadata={
            "question": request.question,
        },
    )
    # try:
    #     langfuse_handler = langfuse_context.get_current_langchain_handler()
    #     res = await summary_workflow.ainvoke(
    #         State(
    #             image_base64=request.image_base64,
    #         ),
    #         config={
    #             "callbacks": [langfuse_handler],
    #             "run_id": request.uuid,
    #         },
    #     )

    # except UnprocessableContentError as e:
    #     raise HTTPException(status_code=422, detail=str(e))
    # except OutputParserException as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # except ValueError as e:
    #     # exceed bedrock rate limit
    #     if "ThrottlingException" in str(e):
    #         raise HTTPException(
    #             status_code=429,
    #             detail="There are so many requests. Please try again later.",
    #         )
    #     raise HTTPException(status_code=500, detail=str(e))

    # langfuse_context.update_current_trace(
    #     name="answer",
    #     user_id=request.user_id,
    #     metadata={
    #         "answer": res["answer"]
    #     },
    # )


    # return ResponseBody(
    #     uuid=request.uuid,
    # )

