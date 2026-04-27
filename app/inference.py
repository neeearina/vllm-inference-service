from vllm import LLM, SamplingParams

model_name = "facebook/opt-125m"
llm = LLM(model=model_name)


def generate_with_vllm(prompt: str, max_tokens: int, temperature: float):
    sampling_params = SamplingParams(
        temperature=temperature,
        top_p=0.95,
        max_tokens=max_tokens,
    )
    outputs = llm.generate(prompts=[prompt], sampling_params=sampling_params)
    
    return outputs[0]
