 # -*- coding: utf-8 -*-
"""
Aplicação Streamlit para reconhecimento de placas de veículos.
Versão com Menu Lateral de Navegação (Principal / Sobre) e Layout Otimizado.
Desenvolvedo com Streamlit, OpenCV, EasyOCR, Rembg e Imutils.

Desenvolvedr: Denilson Alves Oliveira

"""

import streamlit as st
import cv2
import numpy as np
import easyocr
import imutils
import rembg
from PIL import Image

# Configuração global da página
st.set_page_config(
    page_title="Reconhecimento de placas de veículos",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",  # Mantém o menu expandido por padrão
)


def obtenerPlaca(location, img, gray):
    """Extrai a placa a partir da região detectada. (Lógica Intacta)"""
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    imagenContornos = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

    (x, y) = np.where(mask == 255)
    x1, y1 = (np.min(x), np.min(y))
    x2, y2 = (np.max(x), np.max(y))
    cropped_image = gray[x1 : x2 + 1, y1 : y2 + 1]

    imagenplaca = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    reader = easyocr.Reader(["es"])
    result = reader.readtext(cropped_image)

    placa = None
    if result:
        placa = result[0][-2]

    return placa, imagenplaca, imagenContornos


# --- MENU LATERAL DE NAVEGAÇÃO ---
with st.sidebar:
    st.title("🧩 Navegação")
    menu = st.radio(
        "",
        ["Principal", "Sobre"],
        index=0,
        help="Selecione a tela que deseja visualizar."
    )
    st.markdown("---")
    st.caption("Desenvolvido com Streamlit, OpenCV e EasyOCR.")



# TELA 1: PRINCIPAL (RECONHECIMENTO DE PLACAS)

if menu == "Principal":
    # Cabeçalho da Tela Principal
    st.title("🚘 Reconhecimento de Placas de Veículos")
    st.caption("Protótipo de leitura automática utilizando Processamento Digital de Imagens e EasyOCR")

    # Alerta/Instrução estilizada
    st.info("Para começar, faça o upload de uma foto nítida do veículo com a placa visível.", icon="ℹ️")

    archivo_cargado = st.file_uploader("Escolha um arquivo com a imagem do veículo", type=["jpg", "png", "jpeg"])

    if archivo_cargado is not None:
        # Divisão da tela em duas colunas principais equilibradas (Proporção 1:1)
        col_processo, col_resultado = st.columns(2, gap="large")

        # Lê bytes do arquivo e decodifica em BGR
        bytes_data = archivo_cargado.getvalue()
        img = bytes_data
        if type(bytes_data) != np.ndarray:
            imageBGR = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), 1)
            img = imageBGR

        # Feedback visual de carregamento
        with st.spinner("Processando imagem e executando visão computacional..."):
            # Remove fundo (rembg)
            output_array = rembg.remove(img)
            output_image = Image.fromarray(output_array)

            # Converte para tons de cinza e aplica filtro bilateral
            gray = cv2.cvtColor(output_array, cv2.COLOR_BGR2GRAY)
            bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

            # Leitor EasyOCR
            reader = easyocr.Reader(["es"])
            result = reader.readtext(gray)
            resultadosOCR = [x[1] for x in result if len(x[1]) > 4]

            # Detecta bordas com Canny
            edged = cv2.Canny(bfilter, 30, 200)

            # Encontra contornos e seleciona os maiores baseados em área
            keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

            # Loop de busca geométrica pela placa
            location = None
            placa = None
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 10, True)
                if len(approx) == 4:  # Formato retangular esperado
                    location = approx
                    placa, imagenplaca, imagenContornos = obtenerPlaca(location, img, gray)
                    if placa and len(placa) > 5:
                        break

        # --- COLUNA DA ESQUERDA: Linha de Produção (Pipeline) ---
        with col_processo:
            st.subheader("⚙️ Linha de Processamento Digital")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "1. Entrada & Fundo", 
                "2. Tons de Cinza", 
                "3. Filtro de Bordas", 
                "4. Área Isolada"
            ])
            
            with tab1:
                sub_c1, sub_c2 = st.columns(2)
                sub_c1.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Imagem Original", use_container_width=True)
                sub_c2.image(cv2.cvtColor(output_array, cv2.COLOR_BGR2RGB), caption="Fundo Removido (rembg)", use_container_width=True)
                
            with tab2:
                st.image(cv2.cvtColor(bfilter, cv2.COLOR_BGR2RGB), caption="Filtro Bilateral Aplicado", use_container_width=True)
                
            with tab3:
                st.image(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB), caption="Algoritmo Canny (Bordas Estruturais)", use_container_width=True)
                
            with tab4:
                if placa:
                    st.image(imagenContornos, caption="Geometria de 4 Pontos Encontrada", use_container_width=True)
                else:
                    st.info("Nenhum polígono de 4 pontos válido para exibir nesta etapa.")

        # --- COLUNA DA DIREITA: Resultados Finais ---
        with col_resultado:
            st.subheader("🎯 Resultado Final")
            
            if placa:
                with st.container(border=True):
                    res_c1, res_c2 = st.columns([2, 1])
                    
                    with res_c1:
                        text = placa
                        res = cv2.rectangle(img, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)
                        st.image(cv2.cvtColor(res, cv2.COLOR_BGR2RGB), caption="Placa Marcada no Veículo", use_container_width=True)
                    
                    with res_c2:
                        st.metric(label="Texto Identificado", value=text)
                        st.image(imagenplaca, caption="Recorte Enviado ao OCR", use_container_width=True)
                
                st.markdown("---")
                st.write("📋 **Todos os segmentos de texto detectados (Raw OCR):**")
                st.dataframe(resultadosOCR, use_container_width=True)
                
            else:
                st.error("Não foi possível localizar ou interpretar uma placa válida na imagem informada.")
                st.markdown("---")
                st.write("📋 **Textos parciais capturados na imagem (se houver):**")
                st.dataframe(resultadosOCR, use_container_width=True)



# TELA 2: SOBRE (INFORMAÇÕES DO PROJETO)

elif menu == "Sobre":
    st.title("ℹ️ Sobre o Projeto")
    st.markdown("---")
    
    st.markdown("""
    Esta aplicação é um protótipo funcional para o **Reconhecimento Automático de Placas de Veículos (ANPR)**, desenvolvido em Python utilizando técnicas modernas de Processamento Digital de Imagens (PDI) combinadas com Inteligência Artificial para OCR.
    
    ### 🚀 Como funciona o Pipeline de Detecção?
    1. **Remoção de Fundo (`rembg`):** Isole o veículo eliminando ruídos visuais complexos do ambiente ao redor.
    2. **Filtro Bilateral:** Suaviza a textura da imagem reduzindo o ruído digital enquanto preserva com precisão as bordas cruciais da placa.
    3. **Detector de Bordas de Canny:** Mapeia os contornos geométricos da estrutura veicular.
    4. **Aproximação Poligonal:** Varre os contornos em busca de formas quadriláteras estáveis (4 pontos coordenados).
    5. **Segmentação e Extração:** Recorta e mascara apenas a região da placa.
    6. **Reconhecimento Óptico de Caracteres (`EasyOCR`):** Transforma os pixels de caracteres em texto textual puro legível por máquina.
    
    ### 🛠️ Tecnologias Utilizadas
    * **Streamlit:** Construção rápida e estilizada da interface web.
    * **OpenCV (`cv2`):** Biblioteca robusta para todas as operações de visão computacional de baixo nível.
    * **EasyOCR:** Rede Neural profunda especializada na leitura de textos multilíngues em imagens reais.
    * **Rembg:** Modelo de Deep Learning integrado para segmentação de planos de fundo de imagens.
    * **Imutils:** Facilitador de transformações geométricas e manipulação de contornos.
    """)
    
    st.success("Configuração updated e rodando com sucesso!")