import pandas as pd

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
