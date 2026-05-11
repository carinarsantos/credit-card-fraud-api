import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
import os
from pathlib import Path

def train():
    print("Iniciando treinamento do modelo...")
    
    # Caminhos
    data_path = Path("data/creditcard.csv")
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    if not data_path.exists():
        print(f"Erro: Arquivo {data_path} não encontrado!")
        return

    # 1. Carregamento dos dados
    print("Carregando dados...")
    df = pd.read_csv(data_path)
    
    # Normalizamos os nomes das colunas para minúsculas para bater com o schema da API
    df.columns = [col.lower() for col in df.columns]
    
    X = df.drop(columns=['class'])
    y = df['class']
    
    # 2. Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 3. Construção do Pipeline
    # Usamos StandardScaler para as features e RandomForest com pesos balanceados
    print("Treinando Random Forest (isso pode levar alguns minutos)...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(
            n_estimators=100, 
            max_depth=10, 
            random_state=42, 
            class_weight='balanced',
            n_jobs=-1
        ))
    ])
    
    pipeline.fit(X_train, y_train)
    
    # 4. Avaliação básica
    score = pipeline.score(X_test, y_test)
    print(f"Treinamento concluído! Acurácia no teste: {score:.4f}")
    
    # 5. Salvando Artefatos
    print("Salvando modelo e baseline...")
    joblib.dump(pipeline, artifacts_dir / "fraud_model.joblib")
    
    # Salvamos uma amostra das features de teste como baseline para o dashboard de drift
    X_test.head(1000).to_csv(artifacts_dir / "baseline.csv", index=False)
    
    print(f"Artefatos gerados em {artifacts_dir}/")

if __name__ == "__main__":
    train()
