import streamlit as st
import pandas as pd
from db_mongo import inserir_restaurante as inserir_mongo, listar_restaurantes as listar_mongo
from db_sqlite import inserir_restaurante as inserir_sqlite, listar_restaurantes as listar_sqlite
from geoprocessamento import restaurantes_proximos

st.title("Persistência Poliglota - Restaurantes")

# Menu lateral
menu = ["Cadastrar Restaurante", "Listar Restaurantes Mongo", "Listar Restaurantes SQLite", "Buscar Próximos", "Mapa de Restaurantes","Listar Restaurantes Bonitinho"]
opcao = st.sidebar.selectbox("Menu", menu)

# ------------------ Cadastrar ------------------ #
if opcao == "Cadastrar Restaurante":
    st.subheader("Cadastrar Novo Restaurante")
    
    nome = st.text_input("Nome")
    estado = st.text_input("Estado")
    cidade = st.text_input("Cidade")
    cardapio = st.text_area("Cardápio Principal")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    
    avaliacoes_input = st.text_area("Avaliações (separadas por ;)") 
    avaliacoes = avaliacoes_input.split(";") if avaliacoes_input else []

    fotos_input = st.text_area("Fotos (URLs ou caminhos separados por ;)")
    fotos = fotos_input.split(";") if fotos_input else []

    horario_padrao = {
        "segunda": "08:00-18:00",
        "terça": "08:00-18:00",
        "quarta": "08:00-18:00",
        "quinta": "08:00-18:00",
        "sexta": "08:00-18:00",
        "sábado": "08:00-14:00",
        "domingo": "Fechado"
    }

    if st.button("Cadastrar"):
        coordenadas = {"lat": lat, "lon": lon} if lat and lon else None

        # Inserir no SQLite (IDs simplificados)
        estado_id = 1  
        cidade_id = 1  
        inserir_sqlite(nome, estado_id, cidade_id, cardapio)

        # Inserir no MongoDB
        inserir_mongo(nome, estado, cidade, cardapio, coordenadas, avaliacoes, fotos, horario_padrao)

        st.success(f"Restaurante {nome} cadastrado no SQLite e MongoDB!")

# ------------------ Listar Mongo ------------------ #
elif opcao == "Listar Restaurantes Mongo":
    st.subheader("Todos os Restaurantes MongoDB")
    restaurantes = listar_mongo()
    for r in restaurantes:
        st.json(r)

# ------------------ Listar SQLite ------------------ #
elif opcao == "Listar Restaurantes SQLite":
    st.subheader("Todos os Restaurantes SQLite")
    restaurantes = listar_sqlite()
    for r in restaurantes:
        st.write(f"ID: {r[0]}, Nome: {r[1]}, Estado_ID: {r[2]}, Cidade_ID: {r[3]}, Cardápio: {r[4]}")

# ------------------ Buscar Próximos ------------------ #
elif opcao == "Buscar Próximos":
    st.subheader("Restaurantes Próximos")
    lat = st.number_input("Latitude", format="%.6f", key="prox_lat")
    lon = st.number_input("Longitude", format="%.6f", key="prox_lon")
    raio = st.number_input("Raio em km", min_value=1, max_value=50, value=5)
    
    if st.button("Buscar"):
        proximos = restaurantes_proximos(lat, lon, raio)
        if proximos:
            for r in proximos:
                st.json(r)
        else:
            st.warning("Nenhum restaurante encontrado nesse raio.")

# ------------------ Listar Bonitinho ------------------ #
elif opcao == "Listar Restaurantes Bonitinho":
    st.subheader("Restaurantes e Cardápios")
    restaurantes = listar_mongo()
    
    if restaurantes:
        for r in restaurantes:
            st.markdown(f"### {r['nome']}")
            st.write(f"**Estado:** {r['estado']} | **Cidade:** {r['cidade']}")
            st.write(f"**Cardápio:** {r['cardapio_principal']}")
            
            # Avaliações
            if r.get("avaliacoes"):
                st.write("**Avaliações:**")
                for a in r["avaliacoes"]:
                    st.write(f"- {a}")
            
            # Fotos
            if r.get("fotos"):
                st.write("**Fotos:**")
                for f in r["fotos"]:
                    st.image(f, width=200)
            
            # Horário de funcionamento
            if r.get("horario_funcionamento"):
                st.write("**Horário de Funcionamento:**")
                for dia, horario in r["horario_funcionamento"].items():
                    st.write(f"- {dia}: {horario}")
            
            st.markdown("---")
    else:
        st.warning("Nenhum restaurante cadastrado.")

# ------------------ Mapa ------------------ #
elif opcao == "Mapa de Restaurantes":
    st.subheader("Mapa de Restaurantes")
    
    restaurantes = listar_mongo()
    
    # Filtrar só os restaurantes com coordenadas
    data = [
        {"lat": r["coordenadas"]["lat"], "lon": r["coordenadas"]["lon"], "nome": r["nome"]}
        for r in restaurantes if "coordenadas" in r
    ]
    
    if data:
        df = pd.DataFrame(data)
        st.map(df)
        st.write("Restaurantes no mapa:")
        for r in data:
            st.write(f"{r['nome']} ({r['lat']}, {r['lon']})")
    else:
        st.warning("Nenhum restaurante com coordenadas cadastrado.")
