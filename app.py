import streamlit as st
import PyPDF2
import docx

st.set_page_config(page_title="AI Document Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Document Assistant")
st.caption("Республиканский хакатон «Innovation AI Hackathon – 2026» | Направление: AIChatBots")

with st.sidebar:
    st.header("📂 Загрузка документа")
    uploaded_file = st.file_uploader("Выберите PDF или DOCX файл", type=["pdf", "docx"])
    
    extracted_text = ""
    if uploaded_file is not None:
        st.success(f"Файл успешно загружен: **{uploaded_file.name}**")
        if uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        elif uploaded_file.name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                extracted_text += para.text + "\n"
        st.info(f"Считано символов: {len(extracted_text)}")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Загрузите документ слева, и я отвечу на любые вопросы по его содержанию."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Задайте вопрос по документу..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if not extracted_text:
            response = "⚠️ Пожалуйста, сначала загрузите PDF или DOCX файл на панели слева!"
        else:
            response = f"Анализирую документ **{uploaded_file.name}**...\n\nВаш вопрос: '{prompt}'.\n\n*(Здесь модель ИИ формирует ответ на основе текста)*"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})