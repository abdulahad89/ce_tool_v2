import pandas as pd
import os
from sample_data import create_sample_data

def load_data():
    # Auto-create data if not present
    if not os.path.exists("data/conversions.csv") or not os.path.exists("data/engagement.csv"):
        print("Generating sample data...")
        os.makedirs("data", exist_ok=True)
        create_sample_data()

    conv = pd.read_csv("data/conversions.csv")
    eng = pd.read_csv("data/engagement.csv")

    conv = clean_columns(conv)
    eng = clean_columns(eng)

    merged = pd.merge(conv, eng, on="campaign")

    documents = []
    for _, row in merged.iterrows():
        documents.append(str(row.to_dict()))

    return documents
    
def load_data():
    conv = pd.read_csv("data/conversions.csv")
    eng = pd.read_csv("data/engagement.csv")

    merged = pd.merge(conv, eng, on="campaign")

    documents = []

    for _, row in merged.iterrows():
        text = f"""
        Campaign: {row['campaign']}
        Target Conversion: {row['target_conversion']}
        Control Conversion: {row['control_conversion']}
        Incremental Conversion: {row['incremental_conversion']}
        Product Sales: {row['product_sales']}

        Email Clicks: {row['email_clicks']}
        SMS Clicks: {row['sms_clicks']}
        Push Clicks: {row['push_clicks']}
        Web Visits: {row['web_visits']}
        """
        documents.append(text)

    return documents
