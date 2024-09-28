

async def summary(state: State) -> State:
    messages = [
        _SYSTEM_TEMPLATE.format(),
        HumanMessage(content=construct_analyzed_result(state.analyzer_result)),
    ]

    res = await _LLM.ainvoke(messages)
    try:
        summary = NonAggrSummaryInfo.model_validate_json(res.content)
    except ValidationError:
        log.error(f"Failed to parse the response: {res.content}")
        try:
            # Try to parse the response without the Markdown code block syntax
            summary = NonAggrSummaryInfo.model_validate_json(fix_json(res.content))
        except ValidationError:
            log.error(f"Failed to parse the response again")
            new_res = await _LLM.ainvoke(
                messages
                + [
                    AIMessage(res.content),
                    HumanMessage("The response is invalid. Please try again."),
                ]
            )
            summary = NonAggrSummaryInfo.model_validate_json(new_res.content)

    return State(summarizer_result=summary)
