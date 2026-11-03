import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="Comparador Exato de Prontuários", layout="wide")

st.title("🏥 Comparador Exato de Prontuários")
st.write("Cole as duas listas de números abaixo para comparar a igualdade exata e ver as sobras.")

col1, col2 = st.columns(2)

with col1:
    lista_a = st.text_area("Lista A (ex: Relatório / Visitas)", height=250)

with col2:
    lista_b = st.text_area("Lista B (ex: Planilha / Dia/Hip)", height=250)

if st.button("🔍 Comparar Exatamente"):
    # Extrai todos os números mantendo-os exatamente como foram digitados (sem tirar zeros à esquerda)
    # Se quiser considerar como string exata (ex: "0123" diferente de "123"), usamos findall com strings brutas:
    nums_a = re.findall(r'\d+', lista_a) 
    nums_b = re.findall(r'\d+', lista_b)
    
    set_a = set(nums_a)
    set_b = set(nums_b)
    
    # Comparações exatas
    comuns = sorted(list(set_a.intersection(set_b)), key=lambda x: int(x) if x.isdigit() else x)
    sobra_a = sorted(list(set_a.difference(set_b)), key=lambda x: int(x) if x.isdigit() else x)
    sobra_b = sorted(list(set_b.difference(set_a)), key=lambda x: int(x) if x.isdigit() else x)
    
    st.divider()
    
    # Métricas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total na Lista A", len(set_a))
    m2.metric("Total na Lista B", len(set_b))
    m3.metric("Iguais (Comuns)", len(comuns))
    m4.metric("Diferentes / Sobras", len(sobra_a) + len(sobra_b))
    
    st.subheader("📊 Resultados")
    
    tab1, tab2, tab3 = st.tabs([f"✅ Iguais ({len(comuns)})", f"⚠️ Sobraram na Lista A ({len(sobra_a)})", f"⚠️ Sobraram na Lista B ({len(sobra_b)})"])
    
    with tab1:
        if comuns:
            df_comuns = pd.DataFrame(comuns, columns=['Prontuarios Iguais'])
            st.dataframe(df_comuns, use_container_width=True)
        else:
            st.info("Nenhum número em comum.")
            
    with tab2:
        if sobra_a:
            df_sobra_a = pd.DataFrame(sobra_a, columns=['Somente na Lista A'])
            st.dataframe(df_sobra_a, use_container_width=True)
        else:
            st.info("Nada sobrou na Lista A.")
            
    with tab3:
        if sobra_b:
            df_sobra_b = pd.DataFrame(sobra_b, columns=['Somente na Lista B'])
            st.dataframe(df_sobra_b, use_container_width=True)
        else:
            st.info("Nada sobrou na Lista B.")
            
    # Botão de exportação geral em Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(comuns, columns=['Iguais']).to_excel(writer, sheet_name='Iguais', index=False)
        pd.DataFrame(sobra_a, columns=['Apenas_Lista_A']).to_excel(writer, sheet_name='Sobras_Lista_A', index=False)
        pd.DataFrame(sobra_b, columns=['Apenas_Lista_B']).to_excel(writer, sheet_name='Sobras_Lista_B', index=False)
    
    st.download_button("📥 Baixar Relatório Completo em Excel", output.getvalue(), "comparacao_exata_prontuarios.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
