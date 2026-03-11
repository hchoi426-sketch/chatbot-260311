import streamlit as st
from openai import OpenAI

st.title("💬 여행 준비 챗봇")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ✈️ 추천 질문 섹션
    st.markdown("### ✈️ 여행 준비 추천 질문")
    
    suggested_questions = [
        "🧳 여행 짐 싸는 체크리스트를 알려줘",
        "🌍 해외여행 시 필수 준비물은 뭐야?",
        "💊 여행 중 아플 때 대처법은?",
        "💰 여행 경비 절약 꿀팁 알려줘",
        "📱 해외여행 시 유심 vs 로밍 뭐가 나아?",
        "🛂 비자 신청 방법이 궁금해",
        "🏨 숙소 예약할 때 주의할 점은?",
        "🚗 렌터카 이용 시 주의사항은?",
    ]

    # 2열로 버튼 배치
    cols = st.columns(2)
    selected_question = None
    for i, question in enumerate(suggested_questions):
        if cols[i % 2].button(question, use_container_width=True):
            selected_question = question

    st.divider()

    # 기존 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 추천 질문 버튼 클릭 또는 직접 입력 처리
    prompt = selected_question or st.chat_input("여행에 대해 무엇이든 물어보세요! 🌏")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})