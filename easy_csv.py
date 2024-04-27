import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain.llms import ollama
from langchain.llms import HuggingFaceHub
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import speech_recognition as sr
from langchain_community.llms import Ollama

def main():
    load_dotenv()
    st.set_page_config(page_title="Easy CSV", page_icon='📃')
    logo = 'src/img/logo_csv.png'
    st.image(logo, width=150, use_column_width=False)
    st.header('Easy CSV')
    st.subheader('A :blue[IA] que te ajuda com sua planilha :page_with_curl:', divider='rainbow')
    st.header("Pergunte para o seu CSV")
    user_csv = st.file_uploader("Faça o upload do seu CSV", type="csv")

    if user_csv is not None:
        # Criando uma coluna com largura de 2/3 para o input e 1/3 para o botão
        input_column, button_column = st.columns([3, 1])
            # Adicionando o botão com margem superior
        st.markdown(
            """
            <style>
            .stButton>button {
                margin-top: 29px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Inicializa o recognizer
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            # st.write("Pressione o botão abaixo para perguntar por voz.")
            audio_button = button_column.button("Pergunte :studio_microphone:")
            if audio_button:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                try:
                    audio = recognizer.listen(mic)
                    # Reconhece o áudio capturado
                    text = recognizer.recognize_google(audio, language="pt-BR")
                    text = text.lower()
                    st.session_state.user_question = text
                except sr.UnknownValueError:
                    st.write("Não foi possível reconhecer a pergunta.")
                except KeyboardInterrupt:
                    st.write("Gravação interrompida.")

        user_question = input_column.text_input("Faça uma pergunta sobre o seu CSV abaixo ou clique em 'Pergunte' para usar áudio.", st.session_state.get("user_question", ""))
        #0 até 1 -> 0 = menos criativo, 1 = mais criativo
        # Chamar a função dentro do módulo
        llm = OpenAI(temperature=0)
        # llm = ollama.initialize_model(temperature=0)
        #llm = Ollama(model="llama3")
        # llm = ollama(temperature=0)
        #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
        agent = create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question != "":
            response = agent.run(user_question)
            st.subheader(resonse)
            #tradução para PT-BR
            #tradutor = GoogleTranslator(source= "en", target= "pt")
            #traducao = tradutor.translate(response)
            #st.subheader(traducao)

if __name__ == '__main__':
    main()
