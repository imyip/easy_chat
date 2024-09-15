from openai import OpenAI
import streamlit as st
import os

def select_label(option):
    match option:
        case "qwen2:7b-instruct":
            return 'Qwen2-7B模型(无限制)⭐⭐'
        case "llama3.1:8b-instruct-q6_K":
            return 'llama3.1-8b模型(无限制)⭐⭐'
        case "gpt-4o":
           return 'gpt-4o模型⭐⭐⭐⭐'
        case "gpt-4o-mini":
           return 'gpt-4o-mini模型⭐⭐⭐'
        case "meta-llama-3.1-70b-instruct":
            return 'llama3.1-70b模型⭐⭐⭐'
        case "meta-llama-3.1-405b-instruct":
            return 'llama3.1-405b模型⭐⭐⭐⭐'
        case "Qwen/Qwen2-72B-Instruct":
            return 'Qwen2-72B模型⭐⭐⭐'
        case "Qwen/Qwen2-7B-Instruct":
            return 'Qwen2-7B模型⭐⭐'
        case "THUDM/glm-4-9b-chat":
            return 'glm4-9b模型⭐'
        case "cohere-command-r-plus":
            return 'cohere模型⭐⭐'
        case "claude-3-haiku":
            return 'claude-3-haiku模型⭐⭐'
        case "llama-3.1-70b":
            return 'llama-3.1-70b模型⭐⭐'
        case _:
            return '🐻'

def select_change():
    del st.session_state.messages

def get_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

with st.sidebar:
    _model = st.selectbox(
        "选择对话模型",
        ("claude-3-haiku", "llama-3.1-70b", "qwen2:7b-instruct", "llama3.1:8b-instruct-q6_K", "gpt-4o", "gpt-4o-mini", "meta-llama-3.1-70b-instruct", "meta-llama-3.1-405b-instruct","Qwen/Qwen2-72B-Instruct", "Qwen/Qwen2-7B-Instruct", "THUDM/glm-4-9b-chat"),
        8,
        format_func=select_label,
        on_change =select_change,
    )

st.title("🐻 B哥助手")
st.caption("🚀 一个穷人也该使用的人工智能")

system_prompt = "有什么可以帮到你?"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": system_prompt}]

if st.button("清空对话"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    
    _api_key = os.environ.get('SILICONFLOW_KEY')
    _base_url = 'https://api.siliconflow.cn/v1/'

    if _model in ["qwen2:7b-instruct", "llama3.1:8b-instruct-q6_K"]:
        _api_key = 'ollama'
        _base_url = os.environ.get('OLLAMA_URL')
    elif _model in ["gpt-4o", "cohere-command-r-plus", "meta-llama-3.1-70b-instruct"]:
        _api_key =  os.environ.get('GITHUB_MODEL_KEY')
        _base_url = 'https://models.inference.ai.azure.com'
    elif _model in ["THUDM/glm-4-9b-chat", "Qwen/Qwen2-7B-Instruct", "Qwen/Qwen2-72B-Instruct"]:
        _api_key = os.environ.get('SILICONFLOW_KEY')
        _base_url = 'https://api.siliconflow.cn/v1/'
    elif _model in ["meta-llama-3.1-405b-instruct"]:
        _model = "Meta-Llama-3.1-405B-Instruct"
        _api_key = os.environ.get('SAMBOANOVA_KEY')
        _base_url = 'https://api.sambanova.ai/v1/'
    elif _model in ["claude-3-haiku", "llama-3.1-70b", "gpt-4o-mini"]:
        _api_key = "duckduckgo"
        _base_url = 'http://192.168.10.239:56789/v1/'

    client = OpenAI(api_key=_api_key, base_url=_base_url)

    st.chat_message("user").write(prompt)

    with st.chat_message('assistant'):
        st.session_state.messages.append({"role": "user", "content": prompt}) 
        st.session_state.messages.append({"role": "assistant", "content": st.write_stream(get_response(client, _model, st.session_state.messages))})                
