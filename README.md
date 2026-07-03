# Reconhecimento de Placas Veiculares 

![Status do Projeto](https://img.shields.io/badge/status-em_desenvolvimento-yellow)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)


Este projeto foi desenvolvido com o objetivo de identificar, isolar e extrair os caracteres de placas de veículos de forma automatizada. A solução utiliza técnicas de Processamento Digital de Imagens (PDI) e Visão Computacional para processar registros visuais e converter o texto das placas em dados estruturados.

## 📌 Contexto e Objetivos

O sistema visa automatizar o controle de acessos ou triagem de veículos de maneira eficiente, reduzindo a necessidade de verificação manual. O pipeline do projeto abrange desde o recebimento da imagem bruta até a entrega da string correspondente à placa identificada.

---

## 📉 Pipeline de Detecção e Processamento

O fluxo de execução do sistema foi projetado em etapas sequenciais de Visão Computacional e Deep Learning para garantir precisão na leitura:

1. **Remoção de Fundo (`rembg`):** Isole o veículo eliminando ruídos visuais complexos do ambiente ao redor, focando apenas no objeto principal.
2. **Filtro Bilateral:** Suaviza a textura da imagem reduzindo o ruído digital enquanto preserva com precisão as bordas cruciais da placa.
3. **Detector de Bordas de Canny:** Mapeia os contornos geométricos da estrutura veicular para identificar transições de intensidade.
4. **Aproximação Poligonal:** Varre os contornos em busca de formas quadriláteras estáveis (4 pontos coordenados), isolando o retângulo da placa.
5. **Segmentação e Extração:** Recorta e mascara especificamente a Região de Interesse (ROI) correspondente à placa.
6. **Reconhecimento Óptico de Caracteres (EasyOCR):** Transforma os pixels dos caracteres isolados em texto puro legível por máquina.

---

## 🛠️ Tecnologias Utilizadas

O ecossistema técnico do projeto combina bibliotecas clássicas de processamento de imagem com modelos modernos de Deep Learning:

* **Streamlit:** Framework utilizado para a construção rápida, responsiva e estilizada da interface web do usuário.
* **OpenCV (`cv2`):** Biblioteca robusta responsável por todas as operações de visão computacional de baixo nível e manipulação de matrizes de imagem.
* **EasyOCR:** Rede Neural Profunda (Deep Learning) especializada na extração e leitura de textos multilíngues em cenários e imagens reais.
* **Rembg:** Modelo de Deep Learning integrado para a segmentação e remoção automatizada de planos de fundo complexos.
* **Imutils:** Biblioteca auxiliar utilizada para facilitar transformações geométricas, rotações e manipulação simplificada de contornos.
* **Python:** Linguagem base para toda a integração do pipeline e lógica de dados.

* ## 🗂️ Estrutura do Repositório

```text
├── .streamlit/            # Configurações de tema e interface do Streamlit
├── .venv/                 # Ambiente virtual contendo as dependências do projeto
├── Apresentação_projeto.pdf # Documento de apresentação executiva e metodológica
├── main.py                # Script principal e ponto de entrada da aplicação Streamlit
├── placa01.jpeg           # Imagem de teste para validação do pipeline
├── placa02.jpeg           # Imagem de teste para validação do pipeline
├── placa03.jpeg           # Imagem de teste para validação do pipeline
└── requirements.txt       # Lista de bibliotecas e dependências para instalação
