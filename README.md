🍽️ Projeto Persistência Poliglota – Restaurantes

Autores: Ana Beatriz Cavalcanti, Anitta Donato, Rebecca Nery, Ruan Ferreira

## 📖 Introdução

Este projeto tem como objetivo desenvolver uma aplicação prática para gerenciamento de restaurantes, aplicando o conceito de persistência poliglota.

A ideia é integrar diferentes tecnologias de armazenamento de dados em uma única aplicação, explorando as vantagens de cada abordagem:

- SQLite → armazenamento relacional estruturado.

- MongoDB → armazenamento orientado a documentos, flexível e expansível.

- Geoprocessamento → localização de restaurantes próximos a um usuário via coordenadas.

- Streamlit → interface simples e interativa para explorar os dados.

  

## 🏗️ Arquitetura do Sistema

O sistema foi dividido em três módulos principais:

1. Módulo SQLite

- Armazena dados relacionais de restaurantes, estados e cidades.

- Utiliza chaves primárias e estrangeiras para garantir integridade referencial.

- Permite consultas estruturadas e confiáveis.

2. Módulo MongoDB

- Armazena informações completas dos restaurantes:

- Nome, estado, cidade

- Cardápio

- Coordenadas geográficas

- Avaliações

- Fotos

- Horários de funcionamento

- Flexível: permite incluir novos campos sem alterar o esquema.

3. Módulo de Geoprocessamento

- Calcula distâncias geográficas entre coordenadas.

- Permite ao usuário buscar restaurantes próximos a uma localização.

- Interface do Usuário (Streamlit)

- Interface visual interativa.

- Exibição de mapas com a localização dos restaurantes.

- Menu lateral para navegação entre as funcionalidades.

🔧 Pré-requisitos

- Python 3.10+

- Pip atualizado

- SQLite (já incluso no projeto via persistencia.db)

- MongoDB (pode ser local ou Atlas)



## ⚙️ Funcionalidades Principais

```text
✅ Cadastro de Restaurantes – insere dados em SQLite e MongoDB simultaneamente.

✅ Listagem de Restaurantes – mostra informações detalhadas (cardápio, avaliações, fotos, horários).

✅ Busca por Proximidade – retorna apenas restaurantes dentro de um raio definido.

✅ Visualização em Mapa – localização em mapas.
```



## 🔍 Exemplos de Consultas

- Listar todos os restaurantes cadastrados (em SQLite e MongoDB).

- Buscar restaurantes dentro de um raio de 5 km a partir de uma coordenada.

- Exibir informações detalhadas de um restaurante.

- Visualizar todos em um mapa interativo.



## 🖥️ Interface do Usuário

- Menu principal – navegação entre funcionalidades.

- Cadastro de restaurante – formulário intuitivo.

- Listagem – exibe dados em tabelas.

- Mapa – mostra os restaurantes próximos ao usuário.



## 🚀 Como rodar o projeto

1. **Clone o repositório:**
   ``` bash
   git clone https://github.com/RuanVitorr/Persistencia-Poliglota.git
   cd Persistencia-Poliglota
   ```

2. Criar e ativar ambiente virtual (opcional mas recomendado)
``` bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

3. Instalar dependências
``` bash
pip install -r requirements.txt
```

4. Configurar variáveis de ambiente (MongoDB)
Crie um arquivo .env na raiz com:
``` bash
MONGODB_URI=mongodb://localhost:27017/
MONGO_DB=persistencia_poliglota
```

5. Executar a API (FastAPI)
``` bash
uvicorn api_fastapi:app --host 127.0.0.1 --port 8010 --reload
```

6. Executar a interface (Streamlit)
``` bash

streamlit run app_streamlit.py

```
A interface abrirá no navegador (geralmente em http://localhost:8501).



## 🛠️ Estrutura do projeto

```text
📂 Projeto
├── 📄 api_fastapi.py # 🚀 API FastAPI (endpoints REST)
├── 📄 app_streamlit.py # 🎨 Interface Streamlit
├── 🗃️ db_sqlite.py # 🛢️ Conexão/queries SQLite
├── 🗃️ db_mongo.py # 🍃 Conexão/queries MongoDB
├── 🌍 geoprocessamento.py # 📌 Funções geoespaciais
├── 📦 requirements.txt # 📋 Dependências do projeto
└── 💾 persistencia.db # 🗄️ Banco SQLite (exemplo)
```


## ✅ Conclusão

O projeto demonstrou a aplicação prática do conceito de persistência poliglota, integrando SQLite e MongoDB em uma única solução. Além disso, a inclusão do geoprocessamento proporcionou funcionalidades avançadas de localização. A arquitetura modular adotada facilita a expansão futura, permitindo a inclusão de novos tipos de consultas, módulos adicionais ou até novos bancos de dados. A interface interativa desenvolvida com Streamlit garante que os usuários possam acessar as funcionalidades de forma simples e eficiente, tornando o projeto completo e aplicável em cenários reais de gerenciamento de restaurantes.


## 📸 Prints do funcionamento

- Menu principal
- Página de cadastro de restaurante
- Listagem de restaurantes
- Mapa com localização

## 📸 Prints do funcionamento

### Menu Principal

<img width="380" height="852" alt="menu_principal" src="https://github.com/user-attachments/assets/d82ed6e3-619c-4401-bdfb-4619a97a55ee" />


### Cadastro de Restaurante

<img width="568" height="256" alt="cadastro_page" src="https://github.com/user-attachments/assets/4c0a8f2e-36a3-4c8b-88bf-c7da62282fec" />


### Listagem de Restaurantes

<img width="568" height="256" alt="listagem_restau" src="https://github.com/user-attachments/assets/4eff3121-1d4c-4f8f-8870-6c67f7e6b380" />

<img width="568" height="258" alt="listagem_restau2" src="https://github.com/user-attachments/assets/745f8504-e689-4040-929d-a4f21d4dba6d" />


### Mapa Interativo

<img width="568" height="256" alt="localizacao" src="https://github.com/user-attachments/assets/d4bb9b17-45cb-4d81-bd0d-cbb201fd7588" />  
