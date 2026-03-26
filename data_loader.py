import pandas as pd
import os

def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

def load_data():
    conv = pd.read_csv("data/conversions.csv")
    eng = pd.read_csv("data/engagement.csv")

    conv = clean_columns(conv)
    eng = clean_columns(eng)

    # 🔍 Validate keys
    if "campaign_id" not in conv.columns:
        raise ValueError("campaign_id missing in conversions")

    if "campaign_id" not in eng.columns:
        raise ValueError("campaign_id missing in engagement")

    # ✅ AGGREGATE engagement to campaign level
    eng_agg = eng.groupby("campaign_id").agg({
        "spend": "sum",
        "impressions": "sum",
        "clicks": "sum",
        "ctr": "mean",
        "avg_session_duration": "mean",
        "engagement_score": "mean"
    }).reset_index()

    # ✅ Merge
    merged = pd.merge(conv, eng_agg, on="campaign_id", how="left")

    documents = []

    for _, row in merged.iterrows():
        text = f"""
        Campaign ID: {row.get('campaign_id')}
        Campaign Name: {row.get('campaign_name')}

        Segment: {row.get('segment')}
        Treatment: {row.get('treatment')}

        Conversions: {row.get('conversions')}
        Impressions: {row.get('impressions_x')}
        Clicks: {row.get('clicks_x')}
        Conversion Rate: {row.get('conversion_rate')}
        Cost per Conversion: {row.get('cost_per_conversion')}

        Total Spend: {row.get('spend')}
        Total Impressions (Engagement): {row.get('impressions_y')}
        Total Clicks (Engagement): {row.get('clicks_y')}
        Avg CTR: {row.get('ctr')}
        Avg Session Duration: {row.get('avg_session_duration')}
        Engagement Score: {row.get('engagement_score')}
        """

        documents.append(text)

    return documents
