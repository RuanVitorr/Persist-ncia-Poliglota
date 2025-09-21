import os, requests, pandas as pd, streamlit as st

API = os.getenv("API_URL", "http://127.0.0.1:8010")

st.set_page_config(page_title="Restaurantes — Fase 1", page_icon="🍽️", layout="wide")
st.title("Cadastro de Restaurantes — Fase 1 (FastAPI + SQLite)")
st.caption("Obrigatórios: nome, categoria, cidade, estado, país. Extras: faixa_preco ($..$$$$) e nota_media (0–5).")

try:
    health = requests.get(f"{API}/health", timeout=5).json()
    st.success(f"API OK — {health}")
except Exception as e:
    st.error(f"Falha ao conectar na API ({API}). Erro: {e}")

tab_cad, tab_list = st.tabs(["📝 Cadastrar restaurante", "📋 Listar / Editar / Remover"])

with tab_cad:
    st.subheader("Novo restaurante")
    with st.form("form_rest", clear_on_submit=True):
        colA, colB = st.columns([2, 1])
        with colA:
            nome = st.text_input("Nome*", "")
            categoria = st.text_input("Categoria*", "")
            cidade = st.text_input("Cidade*", "")
        with colB:
            estado = st.text_input("Estado (UF)*", "")
            pais = st.text_input("País*", "Brasil")
        col1, col2 = st.columns(2)
        with col1:
            faixa_preco = st.selectbox("Faixa de preço", ["", "$", "$$", "$$$", "$$$$"])
        with col2:
            nota_media = st.number_input("Nota média (0–5)", min_value=0.0, max_value=5.0, step=0.1, value=0.0)
        submitted = st.form_submit_button("Salvar")

    if submitted:
        if not all([nome, categoria, cidade, estado, pais]):
            st.warning("Preencha todos os campos obrigatórios (*)")
        else:
            payload = {
                "nome": nome, "categoria": categoria, "cidade": cidade, "estado": estado, "pais": pais,
                "faixa_preco": faixa_preco or None,
                "nota_media": float(nota_media) if nota_media is not None else None
            }
            r = requests.post(f"{API}/restaurantes", json=payload)
            if r.ok:
                st.success("Restaurante cadastrado!")
            else:
                # Garanta que você está exibindo texto mesmo, não um objeto
                try:
                    # se a API devolver JSON {"detail": "..."}
                    err = r.json()
                    st.error(err.get("detail", str(err)))
                except Exception:
                    st.error(r.text)

with tab_list:
    st.subheader("Restaurantes cadastrados")
    col1, col2 = st.columns([2, 1])

    rlist = requests.get(f"{API}/restaurantes")
    if rlist.ok:
        df = pd.DataFrame(rlist.json())
        if not df.empty:
            with col1:
                st.dataframe(df, use_container_width=True, hide_index=True)
            with col2:
                st.markdown("### Ações")
                rid = st.number_input("ID do restaurante", min_value=1, step=1)

                if st.button("Carregar por ID"):
                    r = requests.get(f"{API}/restaurantes/{int(rid)}")
                    if r.ok:
                        st.success("Sucesso!")
                        try:
                            st.json(r.json())         # exibe o conteúdo de forma segura
                        except Exception:
                            st.text(r.text)
                        else:
                            st.error("Não encontrado.")
                            st.text(r.text)

                st.divider()
                st.markdown("**Editar**")
                nome_e = st.text_input("Novo nome")
                categoria_e = st.text_input("Nova categoria")
                cidade_e = st.text_input("Nova cidade")
                estado_e = st.text_input("Novo estado (UF)")
                pais_e = st.text_input("Novo país")
                faixa_e = st.selectbox("Nova faixa de preço", ["", "$", "$$", "$$$", "$$$$"])
                nota_e = st.number_input("Nova nota média (0–5)", min_value=0.0, max_value=5.0, step=0.1, key="nota_e")
                if st.button("Salvar edição"):
                    if not all([nome_e, categoria_e, cidade_e, estado_e, pais_e]):
                        st.warning("Preencha todos os campos obrigatórios.")
                    else:
                        payload = {
                            "nome": nome_e, "categoria": categoria_e, "cidade": cidade_e,
                            "estado": estado_e, "pais": pais_e,
                            "faixa_preco": faixa_e or None,
                            "nota_media": float(nota_e) if nota_e is not None else None
                        }
                        r = requests.put(f"{API}/restaurantes/{int(rid)}", json=payload)
                        if r.ok:
                            st.success("Restaurante ATUALIZADO!")
                        else:
                            try:
                                err = r.json()
                                st.error(err.get("detail", str(err)))
                            except Exception:
                                st.error(r.text)

                st.divider()
                if st.button("Remover"):
                    r = requests.delete(f"{API}/restaurantes/{int(rid)}")
                    if r.status_code in (200, 204):
                        st.success("Restaurante REMOVIDO!")
                    else:
                        st.error(f"NAO FOI POSSIVEL REMOVER: {r.status_code}")
                        st.error(r.text)
        else:
            st.info("Nenhum restaurante cadastrado ainda.")
    else:
        st.error("Falha ao listar restaurantes.")