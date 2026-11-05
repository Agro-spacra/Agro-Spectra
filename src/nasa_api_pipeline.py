# src/nasa_api_pipeline.py
import requests
import pandas as pd
import numpy as np

def fetch_and_analyze_agro_data(lat, lon, start_date="20260101", end_date="20261101"):
    """
    Fetches NASA POWER meteorological data and evaluates agricultural stress factors:
    Drought, Flooding, Extreme Heat/Fire Risk, and Pest Conditions.
    """
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR,RH2M&community=AG&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
    
    print(f"Connecting to NASA POWER API for coordinates: ({lat}, {lon})...")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        parameters = data.get("properties", {}).get("parameter", {})
        
        # Convert to DataFrame
        df = pd.DataFrame(parameters)
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        
        # Rename columns for clarity
        df.columns = ['Temperature_2M', 'Precipitation', 'Relative_Humidity']
        
        # --- Smart Threshold Analysis (AgroSpectra Logic) ---
        # 1. Extreme Heat & Fire Risk: Temp > 40°C and Humidity < 20%
        df['Fire_Heat_Risk'] = np.where((df['Temperature_2M'] > 40) & (df['Relative_Humidity'] < 20), '🔴 Red - High Fire/Heat Risk', '🟢 Safe')
        
        # 2. Flood / Excess Water Risk: Precipitation > 30mm in a single day
        df['Flood_Risk'] = np.where(df['Precipitation'] > 30, '🟣 Purple - Flood/Excess Water Warning', '🟢 Normal')
        
        # 3. Drought / Water Scarcity: No rain for consecutive days & High Temp
        df['Drought_Risk'] = np.where((df['Precipitation'] == 0) & (df['Temperature_2M'] > 35), '🟡 Yellow - Water Scarcity Alert', '🟢 Optimal')
        
        # 4. Pest & Fungal Proliferation: Warm (20-30°C) + High Humidity (>75%)
        df['Pest_Disease_Risk'] = np.where((df['Temperature_2M'].between(20, 30)) & (df['Relative_Humidity'] > 75), '🟠 Orange -
