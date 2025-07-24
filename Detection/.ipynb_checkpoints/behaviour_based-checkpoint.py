print("🔄 Loading libraries...")
import pandas as pd
import joblib
from Utils.preprocess import preprocess_data
print("✅ Libraries loaded.")
def detect_anomalies(input_csv, model_path="models/anomaly_detector.pkl"):
    """
    Detects anomalies in network traffic using a trained ML model.
    
    Args:
        input_csv (str): Path to the CSV file containing network traffic data.
        model_path (str): Path to the trained ML model.
    
    Returns:
        pd.DataFrame: Data with anomaly predictions.
    """
    # Load network traffic data
    df = pd.read_csv(input_csv)

    # Preprocess the data
    df, label_encoders, scaler = preprocess_data(df, save_csv=False)

    # Load trained anomaly detection model
    model = joblib.load(model_path)

    # Predict anomalies (1 = Normal, -1 = Anomaly)
    df["anomaly"] = model.predict(df)

    # Save results
    df.to_csv("behavior_based_results.csv", index=False)
    print("✅ Behavior-based detection completed. Results saved in 'behavior_based_results.csv'")

    # Print anomalies
    anomalies = df[df["anomaly"] == -1]
    if not anomalies.empty:
        print(f"🚨 {len(anomalies)} anomalies detected!")
    else:
        print("✅ No anomalies detected.")

    return df

# Run behavior-based detection
if __name__ == "__main__":
    detect_anomalies("processed_network_data.csv")
