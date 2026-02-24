import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="RiskGuard - EBIOS RM", page_icon="🛡️", layout="wide")

st.title("🛡️ RiskGuard - Assistant d'Analyse de Risques Cyber")
st.markdown("Basé sur la méthodologie **EBIOS Risk Manager (ANSSI)**.")

if 'assets' not in st.session_state:
    st.session_state['assets'] = []
if 'risks' not in st.session_state:
    st.session_state['risks'] = []

tab1, tab2, tab3 = st.tabs(["1️⃣ Inventaire des Actifs", "2️⃣ Évaluation des Risques", "3️⃣ Matrice & Plan de Traitement"])

# --- ONGLET 1 : INVENTAIRE ---
with tab1:
    st.header("📦 Inventaire des Valeurs Métiers et Biens Supports")
    with st.form("asset_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            asset_name = st.text_input("Nom de l'actif", placeholder="ex: Serveur Base de Données Clients")
        with col2:
            asset_type = st.selectbox("Type d'actif", ["Serveur", "Données", "Utilisateurs", "Application", "Réseau"])
        asset_desc = st.text_area("Description / Sensibilité")
        submit_asset = st.form_submit_button("Ajouter à l'inventaire")
        
        if submit_asset and asset_name:
            st.session_state['assets'].append({
                "ID": f"A{len(st.session_state['assets'])+1}",
                "Nom": asset_name,
                "Type": asset_type,
                "Description": asset_desc
            })
            st.success(f"Actif '{asset_name}' ajouté avec succès !")

    if st.session_state['assets']:
        st.subheader("Actifs actuels")
        st.dataframe(pd.DataFrame(st.session_state['assets']), use_container_width=True)

# --- ONGLET 2 : ÉVALUATION ---
with tab2:
    st.header("⚠️ Évaluation des Événements Redoutés (ER)")
    if not st.session_state['assets']:
        st.info("Veuillez d'abord ajouter des actifs dans l'onglet 'Inventaire'.")
    else:
        with st.form("risk_form", clear_on_submit=True):
            asset_list = [f"{a['ID']} - {a['Nom']}" for a in st.session_state['assets']]
            selected_asset = st.selectbox("Actif ciblé", asset_list)
            threat = st.text_input("Événement Redouté (Menace)", placeholder="ex: Ransomware, Fuite de données, DDoS...")
            
            col1, col2 = st.columns(2)
            with col1:
                impact = st.slider("Impact (Gravité)", 1, 4, 2)
            with col2:
                vraisemblance = st.slider("Vraisemblance (Probabilité)", 1, 4, 2)
            
            submit_risk = st.form_submit_button("Évaluer le risque")
            
            if submit_risk and threat:
                risk_score = impact * vraisemblance
                st.session_state['risks'].append({
                    "Actif": selected_asset,
                    "Menace": threat,
                    "Impact": impact,
                    "Vraisemblance": vraisemblance,
                    "Score": risk_score
                })
                st.success("Risque évalué et enregistré !")

# --- ONGLET 3 : MATRICE & TRAITEMENT (Avec Export) ---
with tab3:
    st.header("📊 Matrice de Risques et Plan de Traitement")
    
    if not st.session_state['risks']:
        st.info("Aucun risque évalué pour le moment. Rendez-vous dans l'onglet 'Évaluation'.")
    else:
        df_risks = pd.DataFrame(st.session_state['risks'])
        
        # Enrichissement du DataFrame avec les recommandations pour l'export
        niveaux = []
        recos = []
        for score in df_risks['Score']:
            if score <= 4:
                niveaux.append("🟢 Faible")
                recos.append("Acceptation du risque. Maintien en conditions de sécurité standards.")
            elif score <= 9:
                niveaux.append("🟠 Modéré")
                recos.append("Mise en place de mesures standards : MFA, sauvegardes, sensibilisation.")
            else:
                niveaux.append("🔴 Critique")
                recos.append("Traitement prioritaire : Chiffrement, segmentation réseau, supervision SOC.")
        
        df_risks['Niveau'] = niveaux
        df_risks['Plan_Action'] = recos

        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("Matrice de Chaleur (Heatmap)")
            fig = go.Figure()
            fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=4.5, y1=4.5, fillcolor="red", opacity=0.2, layer="below", line_width=0)
            fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=3.5, y1=3.5, fillcolor="orange", opacity=0.3, layer="below", line_width=0)
            fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=2.5, y1=2.5, fillcolor="green", opacity=0.3, layer="below", line_width=0)
            fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=1.5, y1=1.5, fillcolor="darkgreen", opacity=0.3, layer="below", line_width=0)

            fig.add_trace(go.Scatter(
                x=df_risks['Vraisemblance'], y=df_risks['Impact'], mode='markers+text',
                marker=dict(size=20, color='black', symbol='circle-open', line_width=3),
                text=df_risks.index + 1, textposition="middle center",
                hovertemplate="<b>%{customdata[0]}</b><br>Impact: %{y}<br>Vraisemblance: %{x}<extra></extra>",
                customdata=df_risks[['Menace']]
            ))
            fig.update_layout(xaxis=dict(title="Vraisemblance", range=[0.5, 4.5], dtick=1), yaxis=dict(title="Impact", range=[0.5, 4.5], dtick=1), width=600, height=600, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📋 Plan de Traitement Automatisé")
            
            # Affichage visuel
            for index, row in df_risks.iterrows():
                with st.expander(f"#{index+1} - {row['Menace']} (Score: {row['Score']})"):
                    st.markdown(f"**Niveau de risque :** {row['Niveau']}")
                    st.markdown(f"**Actif concerné :** {row['Actif']}")
                    st.markdown(f"**Mesures recommandées :** {row['Plan_Action']}")
            
            st.divider()
            
            # Fonction d'export CSV
            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False, sep=";").encode('utf-8')
            
            csv = convert_df(df_risks)
            
            st.download_button(
                label="📥 Exporter le plan d'action (CSV)",
                data=csv,
                file_name='plan_traitement_ebios.csv',
                mime='text/csv',
                type="primary"
            )
