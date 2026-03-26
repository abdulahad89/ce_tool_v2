import pandas as pd
import numpy as np

def create_sample_data():
    campaigns = [f"Campaign_{i}" for i in range(1, 21)]

    # Conversion Table
    conv_data = pd.DataFrame({
        "campaign": campaigns,
        "target_conversion": np.random.randint(100, 500, 20),
        "control_conversion": np.random.randint(50, 300, 20),
        "incremental_conversion": np.random.randint(10, 150, 20),
        "product_sales": np.random.randint(1000, 10000, 20)
    })

    # Engagement Table
    eng_data = pd.DataFrame({
        "campaign": campaigns,
        "email_clicks": np.random.randint(100, 1000, 20),
        "sms_clicks": np.random.randint(50, 500, 20),
        "push_clicks": np.random.randint(30, 300, 20),
        "web_visits": np.random.randint(200, 2000, 20)
    })

    conv_data.to_csv("data/conversions.csv", index=False)
    eng_data.to_csv("data/engagement.csv", index=False)

if __name__ == "__main__":
    create_sample_data()
