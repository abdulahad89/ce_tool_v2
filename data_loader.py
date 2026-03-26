import pandas as pd
import os

# -------------------------------
# Utility: Clean column names
# -------------------------------
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df


# -------------------------------
# Utility: Safe column getter
# -------------------------------
def safe_get(row, col):
    return row[col] if col in row else None


# -------------------------------
# Main Loader
# -------------------------------
def load_data():

    # -------------------------------
    # File existence check
    # -------------------------------
    if not os.path.exists("data/conversions.csv"):
        raise FileNotFoundError("Missing data/conversions.csv")

    if not os.path.exists("data/engagement.csv"):
        raise FileNotFoundError("Missing data/engagement.csv")

    # -------------------------------
    # Load data
    # -------------------------------
    conv = pd.read_csv("data/conversions.csv")
    eng = pd.read_csv("data/engagement.csv")

    # -------------------------------
    # Clean columns
    # -------------------------------
    conv = clean_columns(conv)
    eng = clean_columns(eng)

    print("Conversions Columns:", conv.columns.tolist())
    print("Engagement Columns:", eng.columns.tolist())

    # -------------------------------
    # Validate join key
    # -------------------------------
    if "campaign_id" not in conv.columns:
        raise ValueError(f"'campaign_id' missing in conversions: {conv.columns.tolist()}")

    if "campaign_id" not in eng.columns:
        raise ValueError(f"'campaign_id' missing in engagement: {eng.columns.tolist()}")

    # -------------------------------
    # Aggregate engagement (CRITICAL FIX)
    # -------------------------------
    eng_agg = eng.groupby("campaign_id").agg({
        "spend": "sum",
        "impressions": "sum",
        "clicks": "sum",
        "ctr": "mean",
        "avg_session_duration": "mean",
        "engagement_score": "mean"
    }).reset_index()

    # -------------------------------
    # Merge datasets
    # -------------------------------
    merged = pd.merge(conv, eng_agg, on="campaign_id", how="left")

    documents = []

    # -------------------------------
    # 1️⃣ Campaign-level documents
    # -------------------------------
    for _, row in merged.iterrows():

        text = f"""
        Campaign Overview:

        Campaign ID: {safe_get(row, 'campaign_id')}
        Campaign Name: {safe_get(row, 'campaign_name')}
        Segment: {safe_get(row, 'segment')}
        Treatment: {safe_get(row, 'treatment')}

        Performance Metrics:
        Conversions: {safe_get(row, 'conversions')}
        Impressions: {safe_get(row, 'impressions_x')}
        Clicks: {safe_get(row, 'clicks_x')}
        Conversion Rate: {safe_get(row, 'conversion_rate')}
        Cost per Conversion: {safe_get(row, 'cost_per_conversion')}

        Engagement Summary:
        Total Spend: {safe_get(row, 'spend')}
        Total Impressions: {safe_get(row, 'impressions_y')}
        Total Clicks: {safe_get(row, 'clicks_y')}
        Average CTR: {safe_get(row, 'ctr')}
        Avg Session Duration: {safe_get(row, 'avg_session_duration')}
        Engagement Score: {safe_get(row, 'engagement_score')}
        """

        documents.append(text)

    # -------------------------------
    # 2️⃣ Channel-level documents (BONUS 🔥)
    # -------------------------------
    for _, row in eng.iterrows():

        text = f"""
        Channel Performance:

        Campaign ID: {safe_get(row, 'campaign_id')}
        Channel: {safe_get(row, 'channel')}

        Spend: {safe_get(row, 'spend')}
        Impressions: {safe_get(row, 'impressions')}
        Clicks: {safe_get(row, 'clicks')}
        CTR: {safe_get(row, 'ctr')}
        Avg Session Duration: {safe_get(row, 'avg_session_duration')}
        Engagement Score: {safe_get(row, 'engagement_score')}
        """

        documents.append(text)

    # -------------------------------
    # 3️⃣ Derived Insight Documents (SUPER BONUS 🧠)
    # -------------------------------
    for _, row in merged.iterrows():

        try:
            efficiency = (
                safe_get(row, 'conversions') / safe_get(row, 'spend')
                if safe_get(row, 'spend') not in [0, None]
                else None
            )
        except:
            efficiency = None

        text = f"""
        Derived Insights:

        Campaign ID: {safe_get(row, 'campaign_id')}

        Conversion Efficiency (Conversions / Spend): {efficiency}

        High Engagement Indicator:
        Engagement Score: {safe_get(row, 'engagement_score')}

        Cost Efficiency:
        Cost per Conversion: {safe_get(row, 'cost_per_conversion')}
        """

        documents.append(text)

    print(f"✅ Total Documents Created: {len(documents)}")

    return documents
