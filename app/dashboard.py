import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Configurações de API
API_BASE_URL = os.getenv("API_URL", "http://api:8000/v1")
API_KEY = os.getenv("APP_API_KEY")

st.set_page_config(page_title="Monitor de Detecção de Fraude", layout="wide")

# Inicialização do estado da sessão
if 'v_values' not in st.session_state:
    st.session_state.v_values = {f"v{i}": 0.0 for i in range(1, 29)}
    st.session_state.v_values.update({
        "v1": -1.3598, "v2": -0.0727, "v3": 2.5363, "v4": 1.3781, "v5": -0.3383, "v6": 0.4623
    })
if 'amount' not in st.session_state:
    st.session_state.amount = 149.62
if 'time' not in st.session_state:
    st.session_state.time = 0.0

def send_prediction(payload, sensitivity):
    headers = {"X-API-Key": API_KEY}
    params = {"sensitivity": sensitivity}
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=payload, headers=headers, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def load_fraud_example():
    """Carrega dados reais de uma transação fraudulenta para demonstração"""
    fraud_v = {
        "v1": -2.3122, "v2": 1.9519, "v3": -1.6098, "v4": 3.9979, "v5": -0.5221, "v6": -1.4265,
        "v7": -2.5373, "v8": 1.3916, "v9": -2.7700, "v10": -2.7722, "v11": 3.2020, "v12": -2.8999,
        "v13": -0.5952, "v14": -4.2892, "v15": 0.3897, "v16": -1.1407, "v17": -2.8300, "v18": -0.0168,
        "v19": 0.4169, "v20": 0.1269, "v21": 0.5172, "v22": -0.0350, "v23": -0.4652, "v24": 0.3201,
        "v25": 0.0445, "v26": 0.1778, "v27": 0.2611, "v28": -0.1432
    }
    st.session_state.v_values.update(fraud_v)
    st.session_state.amount = 0.0
    st.session_state.time = 406.0

# Sidebar
st.sidebar.title("💳 Controle de Fraudes")
st.sidebar.markdown("---")
aba = st.sidebar.radio("Navegação", ["🧪 Simulador de Transações", "📊 Monitoramento em Tempo Real", "📉 Análise de Performance"])

# Simulador
if aba == "🧪 Simulador de Transações":
    st.header("🧪 Simulador de Transações")
    st.markdown("Ajuste as variáveis para testar a resposta do modelo em tempo real.")
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("Resetar"):
            st.session_state.v_values = {f"v{i}": 0.0 for i in range(1, 29)}
            st.session_state.amount = 150.0
            st.rerun()
    with col_btn2:
        if st.button("🚨 Carregar Exemplo de Fraude Real"):
            load_fraud_example()
            st.rerun()

    with st.form("form_simulador"):
        st.subheader("Dados Básicos")
        c1, c2, c3 = st.columns(3)
        with c1:
            amount = st.number_input("Valor (Amount)", min_value=0.0, value=st.session_state.amount, step=10.0)
        with c2:
            time = st.number_input("Tempo (Segundos)", min_value=0.0, value=st.session_state.time)
        with c3:
            sensitivity = st.slider("Sensibilidade do Modelo", 0.0, 1.0, 0.5)

        st.subheader("Variáveis de Comportamento (V1 - V6)")
        cv1, cv2, cv3 = st.columns(3)
        v_inputs = {}
        for i in range(1, 7):
            col = [cv1, cv2, cv3][(i-1)%3]
            v_inputs[f"v{i}"] = col.number_input(f"V{i}", value=st.session_state.v_values[f"v{i}"], format="%.4f")
        
        with st.expander("🛠️ Variáveis Avançadas (V7 - V28)"):
            st.caption("Componentes principais (PCA) com impacto direto na decisão do modelo.")
            av_cols = st.columns(4)
            for i in range(7, 29):
                col = av_cols[(i-7)%4]
                v_inputs[f"v{i}"] = col.number_input(f"V{i}", value=st.session_state.v_values[f"v{i}"], format="%.4f")

        submitted = st.form_submit_button("🚀 Analisar Transação")
        
        if submitted:
            payload = {"time": time, "amount": amount}
            payload.update(v_inputs)
            
            with st.spinner("Analisando..."):
                result = send_prediction(payload, sensitivity)
            
            if "error" in result:
                st.error(f"Erro na API: {result['error']}")
            else:
                prob = result.get("probability", 0)
                is_fraud = result.get("is_fraud", False)
                
                if is_fraud:
                    st.error(f"🚨 ALERTA DE FRAUDE DETECTADA! Probabilidade: {prob*100:.2f}%")
                else:
                    st.success(f"✅ Transação Legítima. Probabilidade de fraude: {prob*100:.2f}%")
                
                with st.expander("Ver Detalhes Técnicos (JSON)"):
                    st.json(result)

# Monitoramento
elif aba == "📊 Monitoramento em Tempo Real":
    st.header("📊 Monitoramento em Tempo Real")
    
    if st.button("🔄 Atualizar Dados"):
        headers = {"X-API-Key": API_KEY}
        try:
            response = requests.get(f"{API_BASE_URL}/logs?limit=500", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    df['created_at'] = pd.to_datetime(df['created_at'])
                    
                    m1, m2, m3 = st.columns(3)
                    total = len(df)
                    frauds = df['is_fraud'].sum()
                    avg_lat = df['processing_time_ms'].mean()
                    
                    m1.metric("Total de Requisições", total)
                    m2.metric("Fraudes Detectadas", frauds, delta=f"{(frauds/total)*100 if total > 0 else 0:.1f}%", delta_color="inverse")
                    m3.metric("Latência Média", f"{avg_lat:.2f} ms")

                    st.markdown("---")
                    
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        fig_lat = px.line(df, x='created_at', y='processing_time_ms', 
                                          title="Velocidade de Resposta",
                                          labels={'created_at': 'Horário', 'processing_time_ms': 'Tempo (ms)'})
                        fig_lat.update_traces(line_color='#00CC96')
                        st.plotly_chart(fig_lat, use_container_width=True)
                    
                    with c2:
                        df_plot = df.copy()
                        df_plot['Status'] = df_plot['is_fraud'].map({True: 'Fraude', False: 'Legítima'})
                        fig_dist = px.pie(df_plot, names='Status', title="Distribuição",
                                          color='Status', color_discrete_map={'Legítima': '#636EFA', 'Fraude': '#EF553B'})
                        st.plotly_chart(fig_dist, use_container_width=True)
                    
                    st.subheader("Histórico de Transações")
                    df_display = df[['transaction_id', 'is_fraud', 'prediction_score', 'processing_time_ms', 'created_at', 'status']].copy()
                    df_display.columns = ['ID Transação', 'É Fraude?', 'Score', 'Latência (ms)', 'Horário', 'Status API']
                    st.dataframe(df_display, use_container_width=True)
                else:
                    st.info("Nenhum dado encontrado.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")

# Performance
elif aba == "📉 Análise de Performance":
    st.header("📉 Análise de Performance")
    
    baseline_path = "artifacts/baseline.csv"
    if os.path.exists(baseline_path):
        df_base = pd.read_csv(baseline_path)
        st.subheader("Distribuição de Valor (Baseline de Treino)")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df_base['amount'], name="Treino", marker_color='#636EFA', opacity=0.6))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Baseline não encontrada.")