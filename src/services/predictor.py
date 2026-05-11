import joblib
import numpy as np
import pandas as pd
from pathlib import Path

class FraudPredictor:
    """Encapsula a lógica de carregamento e inferência do modelo ML."""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.pipeline = None

    def load_model(self):
        """Carrega o pipeline serializado do disco."""
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Modelo não encontrado em: {self.model_path}")
        self.pipeline = joblib.load(self.model_path)

    def predict(self, features_dict: dict, threshold: float = 0.5) -> tuple[bool, float]:
        """Realiza a inferência a partir de um dicionário de features."""
        if self.pipeline is None:
            raise RuntimeError("Modelo não carregado.")

        # Converte para DataFrame mantendo a compatibilidade de colunas
        df_input = pd.DataFrame([features_dict])
        
        # Probabilidade da classe positiva (Fraude)
        probability = self.pipeline.predict_proba(df_input)[0][1]
        
        # Classificação baseada no threshold de sensibilidade
        prediction = bool(probability >= threshold)
        
        return prediction, float(probability)