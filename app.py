import streamlit as st
from scraper import buscar_en_imperial

st.set_page_config(page_title="Buscador Imperial")

st.title("🔍 Buscador de Materiales")
st.write("Escribe el producto que necesitas para ver disponibilidad y precio.")

termino = st.text_input("Buscar producto:", "puerta")

if st.button("Buscar en Imperial"):
    with st.spinner('Buscando...'):
        try:
            df = buscar_en_imperial(termino)
            if not df.empty:
                st.table(df)
            else:
                st.warning("No se encontraron resultados.")
        except Exception as e:
            st.error(f"Error al buscar: {e}")
