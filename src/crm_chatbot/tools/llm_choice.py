from typing import Optional
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

def instantiate_chatllm(maker: str="ollama", model: str="llama3.2", temperature: Optional[float]=None) -> ChatAnthropic | ChatOpenAI | ChatOllama:
    match maker:
        case 'anthropic':
            if not model:
                llm = ChatAnthropic(model=model, temperature=temperature)
            else:
                # Haiku is faster and cheaper, but less accurate
                # llm = ChatAnthropic(model="claude-3-haiku-20240307")
                llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=temperature)
        case 'openai':
            if not model:
                # temperature defaults to 0.7
                llm = ChatOllama(model=model, temperature=temperature)
            else: 
                llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=temperature)
        case 'ollama':
            if not model:
                llm = ChatOllama(model=model, temperature=temperature)
            else:
                # temperature defaults to 0.8
                # qwen2.5:14b is the best in handling questions and arithmetic comparing to gemma2 and llama3.2 
                # llama3.2 is a better choice for tool calling than qwen2.5:14b
                llm = ChatOllama(model='qwen2.5:14b', temperature=temperature)

    return llm
