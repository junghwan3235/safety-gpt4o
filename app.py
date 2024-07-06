import os
import streamlit as st
from openai import OpenAI
import base64
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

st.set_page_config(page_title="Image Analyst", layout="centered", initial_sidebar_state="collapsed")
st.title(":construction_worker: 숨은 안전 찾기 :construction_worker:")
st.header(":blue[_작업 안전에 대해 도움을 드리겠습니다_]")

# .env 파일에서 OpenAI API Key를 로드합니다.
api_key = os.getenv("OPENAI_API_KEY")

def get_image_description(client, uploaded_file, prompt):
    # Encode the uploaded image in base64
    encoded_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

    # Create the GPT-4o API request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                    },
                ],
            }
        ],
        max_tokens=1200,
    )

    # Extract and return the description
    return response.choices[0].message.content

if api_key:
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # 사용자로부터 이미지 업로드를 위한 파일 업로더
    uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"], key="file_uploader_1")

    if uploaded_file:
        # 업로드된 이미지 표시
        with st.expander("이미지", expanded=True):
            st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

    show_details = st.checkbox("안전에 대한 질문이나 사진의 세부 정보 추가", value=True, key="checkbox1")

    if show_details:
        additional_details = st.text_area(
            "안전에 궁금한 점을 입력해주세요:",
            key="additional_details_1",
            disabled=not show_details
        )

    analyze_button = st.button("안전 이미지 분석하기")

    if uploaded_file is not None and analyze_button:
        with st.spinner("이미지를 분석 중입니다 ..."):
            # 추가 세부 정보와 함께 최적화된 프롬프트 텍스트
            prompt_text = (
                "당신은 매우 지식이 풍부한 안전관리 이미지 분석 전문가입니다. "
                "다음 이미지를 자세히 검토하는 것이 당신의 임무입니다. "
                "이미지가 묘사하는 것에 대한 안전관리 규정에 의거한 정확한 설명을 제공하세요. "
                "주요 요소와 그 중요성을 강조하고, 분석 결과를 명확하고 잘 구조화된 마크다운 형식으로 제시하세요. "
                "해당되는 경우, 설명을 향상시키기 위해 관련 안전관리 용어를 포함하세요. "
                "독자가 안전에 대한 기본적인 이해를 가지고 있다고 가정합니다."
                "짧게 설명하는 굵은 글씨로 자세한 이미지 캡션을 생성하세요."
            )

            if show_details and additional_details:
                prompt_text += f"\n\n사용자가 제공한 추가 맥락:\n{additional_details}"

            # OpenAI API에 요청
            try:
                description = get_image_description(client, uploaded_file, prompt_text)
                st.markdown(description)
            except Exception as e:
                st.error(f"오류 발생: {e}")
else:
    st.error("유효한 OpenAI API 키를 제공해 주세요.")

# Streamlit app layout
st.title(":construction_worker: TBM Helper :construction_worker:")
st.header(":blue[_TBM 대해 도움을 드리겠습니다_]")

# 사용자로부터 이미지 업로드를 위한 파일 업로더
uploaded_file2 = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"], key="file_uploader_2")

if uploaded_file2:
    # 업로드된 이미지 표시
    with st.expander("이미지", expanded=True):
        st.image(uploaded_file2, caption=uploaded_file2.name, use_column_width=True)

# 이미지에 대한 추가 세부 정보 입력 표시 여부를 결정하는 토글
show_details = st.checkbox("안전에 대한 질문이나 사진의 세부 정보 추가", value=True, key="checkbox2")

if show_details:
    # 추가 세부 정보를 위한 텍스트 입력 영역, 토글이 True인 경우에만 표시됨
    additional_details = st.text_area(
        "안전에 궁금한 점을 입력해주세요:",
        key="additional_details_2",
        disabled=not show_details
    )

# 분석을 시작하기 위한 버튼
analyze_button2 = st.button("TBM 이미지 분석하기")

# 이미지가 업로드되었고 버튼이 눌렸는지 확인
if uploaded_file2 is not None and analyze_button2:

    with st.spinner("이미지를 분석 중입니다 ..."):
        # 추가 세부 정보와 함께 최적화된 프롬프트 텍스트
        prompt_text = (
            "당신은 매우 지식이 풍부한 안전관리 이미지 분석 전문가입니다. "
            "이미지를 바탕으로 착용하고 있는 안전 장비를 식별하고, 정보통신 공사 표준 안전 장비 체크리스트와 비교하는 것이 당신의 임무입니다. "
            "올바르게 착용한 장비는 각각 나열하고, 누락되거나 제대로 사용되지 않은 장비가 있으면 식별해 주세요 ."
            "작업자가 안전 규정을 완전히 준수하려면 어떤 조치를 취해야 하는지 추천해 주세요"
            "주요 요소와 그 중요성을 강조하고, 분석 결과를 명확하고 잘 구조화된 마크다운 형식으로 제시하세요. "
            "해당되는 경우, 설명을 향상시키기 위해 관련 안전관리 용어를 포함하세요. 한글로 답해주세요 "
            "독자가 안전에 대한 기본적인 이해를 가지고 있다고 가정합니다."
            "짧게 설명하는 굵은 글씨로 자세한 이미지 캡션을 생성하세요."
            "어떤 작업을 하는지 아래 추가정보를 활용해 작업에 맞는 안전 장비를 우선 고려해주세요"
        )

        if show_details and additional_details:
            prompt_text += (
                f"\n\n사용자가 제공한 추가 맥락:\n{additional_details}"
            )

        # OpenAI API에 요청
        try:
            # Initialize the OpenAI client
            api_key = os.environ.get("OPENAI_API_KEY", "")
            client = OpenAI(api_key=api_key)

            # Get the image description
            description = get_image_description(client, uploaded_file2, prompt_text)
            st.markdown(description)
        except Exception as e:
            st.error(f"오류 발생: {e}")
else:
    # 사용자가 해야 할 작업에 대한 경고 표시
    if not uploaded_file2 and analyze_button2:
        st.warning("TBM 이미지를 업로드해주세요.")