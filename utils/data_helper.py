# utils/data_helper.py
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, precision_recall_curve, confusion_matrix

np.random.seed(42)

def generate_telecom_cohorts():
    n_samples = 7043
    genders = np.random.choice(['Female', 'Male'], size=n_samples)
    senior_citizen = np.random.choice([0, 1], size=n_samples, p=[0.84, 0.16])
    partner = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.48, 0.52])
    dependents = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.30, 0.70])
    contracts = np.random.choice(['Month-to-month', 'One year', 'Two year'], size=n_samples, p=[0.55, 0.24, 0.21])
    paperless = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.59, 0.41])
    payments = np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], size=n_samples, p=[0.34, 0.23, 0.22, 0.21])
    
    tenure = np.zeros(n_samples, dtype=int)
    for i, contract in enumerate(contracts):
        if contract == 'Month-to-month':
            tenure[i] = np.random.choice(np.arange(1, 25), p=np.linspace(2, 0.1, 24)/np.linspace(2, 0.1, 24).sum())
        elif contract == 'One year':
            tenure[i] = np.random.randint(12, 60)
        else:
            tenure[i] = np.random.randint(36, 73)
            
    internet = np.random.choice(['DSL', 'Fiber optic', 'No'], size=n_samples, p=[0.34, 0.44, 0.22])
    phone = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.90, 0.10])
    
    multiple_lines, online_sec, online_bac, dev_prot, tech_sup, stream_tv, stream_mov = [], [], [], [], [], [], []
    for i in range(n_samples):
        multiple_lines.append(np.random.choice(['Yes', 'No', 'No phone service'], p=[0.42, 0.48, 0.10] if phone[i] == 'Yes' else [0, 0, 1]))
        if internet[i] == 'No':
            online_sec.append('No internet service'); online_bac.append('No internet service'); dev_prot.append('No internet service')
            tech_sup.append('No internet service'); stream_tv.append('No internet service'); stream_mov.append('No internet service')
        else:
            online_sec.append(np.random.choice(['Yes', 'No'], p=[0.35, 0.65]))
            online_bac.append(np.random.choice(['Yes', 'No'], p=[0.40, 0.60]))
            dev_prot.append(np.random.choice(['Yes', 'No'], p=[0.40, 0.60]))
            tech_sup.append(np.random.choice(['Yes', 'No'], p=[0.35, 0.65]))
            stream_tv.append(np.random.choice(['Yes', 'No'], p=[0.45, 0.55]))
            stream_mov.append(np.random.choice(['Yes', 'No'], p=[0.45, 0.55]))
            
    monthly_charges = np.zeros(n_samples)
    for i in range(n_samples):
        base = 20.0
        if internet[i] == 'DSL': base += 35.0
        elif internet[i] == 'Fiber optic': base += 55.0
        monthly_charges[i] = base + np.random.uniform(-5.0, 5.0)
        
    total_charges = monthly_charges * tenure
    churn_prob = np.zeros(n_samples)
    for i in range(n_samples):
        p = 0.05
        if contracts[i] == 'Month-to-month': p += 0.35
        if internet[i] == 'Fiber optic': p += 0.25
        if tenure[i] <= 12: p += 0.20
        churn_prob[i] = min(max(p, 0.02), 0.95)
        
    churn = np.where(np.random.rand(n_samples) < churn_prob, 'Yes', 'No')
    
    df = pd.DataFrame({
        'customerID': [f'{np.random.randint(1000, 9999)}-A' for _ in range(n_samples)],
        'gender': genders, 'SeniorCitizen': senior_citizen, 'Partner': partner, 'Dependents': dependents,
        'tenure': tenure, 'PhoneService': phone, 'MultipleLines': multiple_lines, 'InternetService': internet,
        'OnlineSecurity': online_sec, 'OnlineBackup': online_bac, 'DeviceProtection': dev_prot, 'TechSupport': tech_sup,
        'StreamingTV': stream_tv, 'StreamingMovies': stream_mov, 'Contract': contracts, 'PaperlessBilling': paperless,
        'PaymentMethod': payments, 'MonthlyCharges': monthly_charges, 'TotalCharges': total_charges, 'Churn': churn
    })
    
    scaler = StandardScaler()
    scaled_feats = scaler.fit_transform(df[['tenure', 'MonthlyCharges']])
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(scaled_feats)
    
    cluster_mapping = {}
    for cluster_id in range(4):
        c_mean_tenure = df[df['Cluster'] == cluster_id]['tenure'].mean()
        c_mean_spend = df[df['Cluster'] == cluster_id]['MonthlyCharges'].mean()
        if c_mean_tenure < 24 and c_mean_spend < 50:
            cluster_mapping[cluster_id] = "New / Budget"
        elif c_mean_tenure < 24 and c_mean_spend >= 50:
            cluster_mapping[cluster_id] = "High-Spend / High-Risk"
        elif c_mean_tenure >= 24 and c_mean_spend < 50:
            cluster_mapping[cluster_id] = "Loyal / Budget"
        else:
            cluster_mapping[cluster_id] = "High-Value / Loyal"
            
    df['SegmentName'] = df['Cluster'].map(cluster_mapping)
    return df

def train_and_evaluate_models(df):
    cat_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']
    df_encoded = df.copy()
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    df_encoded['Churn'] = df_encoded['Churn'].map({'Yes': 1, 'No': 0})
    
    features = cat_cols + ['tenure', 'MonthlyCharges', 'TotalCharges']
    X = df_encoded[features]
    y = df_encoded['Churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.fit_transform(X_train[['tenure', 'MonthlyCharges', 'TotalCharges']])
    X_test_scaled[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.transform(X_test[['tenure', 'MonthlyCharges', 'TotalCharges']])
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    }
    evaluation_metrics = {}
    fitted_models = {}
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        prec, rec_vals, _ = precision_recall_curve(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        evaluation_metrics[name] = {
            'accuracy': accuracy_score(y_test, y_pred), 'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred), 'f1': f1_score(y_test, y_pred), 'roc_auc': auc(fpr, tpr),
            'fpr': fpr, 'tpr': tpr, 'precision_curve': prec, 'recall_curve': rec_vals, 'confusion_matrix': cm
        }
        fitted_models[name] = model
    return fitted_models, evaluation_metrics, scaler, label_encoders, features
