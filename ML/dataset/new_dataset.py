import pandas as pd
import numpy as np
import random

# Load existing data
data = pd.read_csv('dataset/Crop_recommendation.csv')

# Number of rows to generate
target_rows = int(input("Enter the number of rows to generate: "))
current_rows = len(data)
rows_to_generate = target_rows - current_rows

# Define possible values for categorical columns
regions = ["Northern", "Southern", "Eastern", "Western", "Central"]
soil_types = ["Sandy", "Loamy", "Clay", "Sandy Loam", "Clay Loam", "Silty", "Alluvial", "Red", "Black", "Loamy Sand"]
growing_seasons = ["Summer", "Winter", "Spring", "Monsoon", "Rainy", "Rabi", "Kharif", "Perennial"]
irrigation_methods = ["Flood", "Drip", "Sprinkler"]
pest_incidents = ["None", "Low", "Medium", "High"]
fertilizer_applications = ["Low", "Medium", "High"]
water_sources = ["Canal", "Well", "Rain", "River", "Reservoir"]
crop_rotation_options = ["Fallow", "Rice", "Wheat", "Maize", "Cotton", "Pulses", "Vegetables", "Oilseeds", "Sugarcane"]

# Map crops to typical values (to make the synthetic data more realistic)
crop_properties = {
    'rice': {
        'regions': ["Eastern", "Southern"],
        'soil_types': ["Clay", "Alluvial"],
        'growing_seasons': ["Kharif", "Monsoon"],
        'yield_range': (2000, 6000),
        'growth_days': (110, 150),
        'irrigation': ["Flood"],
        'pest_incidents': ["Low", "Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (100, 180),
        'organic_matter': (1.0, 3.0),
        'crop_rotation': ["Fallow", "Pulses", "Vegetables"],
        'seed_rate': (40, 60),
        'market_price': (0.2, 0.5),
        'water_sources': ["Canal", "River", "Reservoir"]
    },
    'maize': {
        'regions': ["Northern", "Southern", "Central"],
        'soil_types': ["Loamy", "Sandy Loam"],
        'growing_seasons': ["Kharif", "Rabi"],
        'yield_range': (2500, 8000),
        'growth_days': (80, 110),
        'irrigation': ["Flood", "Sprinkler"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (120, 200),
        'organic_matter': (1.2, 3.5),
        'crop_rotation': ["Rice", "Pulses", "Vegetables", "Cotton"],
        'seed_rate': (18, 25),
        'market_price': (0.15, 0.35),
        'water_sources': ["Well", "Canal", "Rain"]
    },
    'chickpea': {
        'regions': ["Central", "Northern"],
        'soil_types': ["Loamy", "Clay Loam"],
        'growing_seasons': ["Rabi", "Winter"],
        'yield_range': (920, 1800),
        'growth_days': (90, 120),
        'irrigation': ["Sprinkler", "Flood"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Low", "Medium"],
        'fertilizer_kg_ha': (30, 80),
        'organic_matter': (0.8, 2.5),
        'crop_rotation': ["Wheat", "Rice", "Fallow"],
        'seed_rate': (70, 90),
        'market_price': (0.6, 1.2),
        'water_sources': ["Rain", "Well"]
    },
    'kidneybeans': {
        'regions': ["Northern", "Western"],
        'soil_types': ["Sandy Loam", "Loamy"],
        'growing_seasons': ["Rabi", "Summer"],
        'yield_range': (1000, 2000),
        'growth_days': (85, 110),
        'irrigation': ["Drip", "Sprinkler"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Low", "Medium"],
        'fertilizer_kg_ha': (40, 80),
        'organic_matter': (1.0, 2.8),
        'crop_rotation': ["Maize", "Vegetables", "Wheat"],
        'seed_rate': (60, 80),
        'market_price': (0.7, 1.5),
        'water_sources': ["Well", "Rain", "Canal"]
    },
    'pigeonpeas': {
        'regions': ["Central", "Southern"],
        'soil_types': ["Red", "Loamy"],
        'growing_seasons': ["Kharif", "Monsoon"],
        'yield_range': (950, 1800),
        'growth_days': (120, 180),
        'irrigation': ["Flood", "Drip"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Low", "Medium"],
        'fertilizer_kg_ha': (30, 70),
        'organic_matter': (0.8, 2.2),
        'crop_rotation': ["Rice", "Cotton", "Fallow"],
        'seed_rate': (15, 20),
        'market_price': (0.6, 1.2),
        'water_sources': ["Rain", "Well"]
    },
    'mothbeans': {
        'regions': ["Western", "Central"],
        'soil_types': ["Sandy", "Loamy Sand"],
        'growing_seasons': ["Kharif"],
        'yield_range': (920, 1500),
        'growth_days': (65, 90),
        'irrigation': ["Sprinkler", "Flood"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Low"],
        'fertilizer_kg_ha': (20, 60),
        'organic_matter': (0.7, 2.0),
        'crop_rotation': ["Maize", "Millet", "Fallow"],
        'seed_rate': (12, 18),
        'market_price': (0.7, 1.3),
        'water_sources': ["Rain", "Well"]
    },
    'mungbean': {
        'regions': ["Northern", "Central"],
        'soil_types': ["Sandy Loam", "Loamy"],
        'growing_seasons': ["Kharif", "Spring"],
        'yield_range': (950, 1700),
        'growth_days': (70, 90),
        'irrigation': ["Sprinkler", "Flood"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Low", "Medium"],
        'fertilizer_kg_ha': (30, 70),
        'organic_matter': (0.8, 2.5),
        'crop_rotation': ["Rice", "Wheat", "Vegetables"],
        'seed_rate': (15, 25),
        'market_price': (0.6, 1.2),
        'water_sources': ["Well", "Rain", "Canal"]
    },
    'blackgram': {
        'regions': ["Southern", "Central"],
        'soil_types': ["Clay Loam", "Black"],
        'growing_seasons': ["Kharif", "Rabi"],
        'yield_range': (920, 1600),
        'growth_days': (70, 90),
        'irrigation': ["Flood", "Sprinkler"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Low", "Medium"],
        'fertilizer_kg_ha': (30, 70),
        'organic_matter': (1.0, 2.5),
        'crop_rotation': ["Rice", "Cotton", "Vegetables"],
        'seed_rate': (15, 20),
        'market_price': (0.7, 1.3),
        'water_sources': ["Rain", "Well", "Canal"]
    },
    'lentil': {
        'regions': ["Northern", "Central"],
        'soil_types': ["Loamy", "Sandy Loam"],
        'growing_seasons': ["Rabi", "Winter"],
        'yield_range': (950, 1800),
        'growth_days': (100, 120),
        'irrigation': ["Sprinkler", "Drip"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Low", "Medium"],
        'fertilizer_kg_ha': (30, 60),
        'organic_matter': (0.8, 2.2),
        'crop_rotation': ["Wheat", "Rice", "Fallow"],
        'seed_rate': (35, 45),
        'market_price': (0.8, 1.6),
        'water_sources': ["Well", "Canal", "Rain"]
    },
    'pomegranate': {
        'regions': ["Western", "Southern"],
        'soil_types': ["Loamy", "Sandy Loam"],
        'growing_seasons': ["Perennial"],
        'yield_range': (8000, 18000),
        'growth_days': (365, 730),
        'irrigation': ["Drip"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (150, 300),
        'organic_matter': (1.5, 4.0),
        'crop_rotation': ["Fallow", "Vegetables"],
        'seed_rate': (1, 2),  # Plants per sq meter
        'market_price': (1.2, 2.5),
        'water_sources': ["Well", "Canal", "Reservoir"]
    },
    'banana': {
        'regions': ["Southern", "Eastern"],
        'soil_types': ["Loamy", "Alluvial"],
        'growing_seasons': ["Perennial"],
        'yield_range': (25000, 42500),
        'growth_days': (300, 450),
        'irrigation': ["Drip", "Flood"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["High"],
        'fertilizer_kg_ha': (250, 500),
        'organic_matter': (2.0, 5.0),
        'crop_rotation': ["Fallow", "Vegetables"],
        'seed_rate': (1600, 2000),  # Plants/ha
        'market_price': (0.4, 0.9),
        'water_sources': ["Well", "Canal", "River"]
    },
    'mango': {
        'regions': ["Southern", "Western"],
        'soil_types': ["Loamy", "Sandy Loam", "Red"],
        'growing_seasons': ["Perennial"],
        'yield_range': (8000, 25000),
        'growth_days': (1460, 1825),
        'irrigation': ["Drip", "Flood"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (200, 400),
        'organic_matter': (1.8, 4.5),
        'crop_rotation': ["Fallow"],
        'seed_rate': (100, 150),  # Trees/ha
        'market_price': (0.8, 2.0),
        'water_sources': ["Well", "Canal", "River"]
    },
    'grapes': {
        'regions': ["Western", "Southern"],
        'soil_types': ["Sandy Loam", "Loamy"],
        'growing_seasons': ["Perennial"],
        'yield_range': (12000, 25000),
        'growth_days': (730, 1095),
        'irrigation': ["Drip"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (180, 350),
        'organic_matter': (1.5, 4.0),
        'crop_rotation': ["Fallow", "Vegetables"],
        'seed_rate': (1200, 1800),  # Vines/ha
        'market_price': (1.0, 2.2),
        'water_sources': ["Well", "Canal"]
    },
    'watermelon': {
        'regions': ["Southern", "Western"],
        'soil_types': ["Sandy", "Sandy Loam"],
        'growing_seasons': ["Summer", "Spring"],
        'yield_range': (15000, 30000),
        'growth_days': (80, 110),
        'irrigation': ["Drip", "Sprinkler"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (120, 200),
        'organic_matter': (1.0, 3.0),
        'crop_rotation': ["Rice", "Vegetables", "Fallow"],
        'seed_rate': (2, 3),  # kg/ha
        'market_price': (0.2, 0.5),
        'water_sources': ["Well", "Canal", "River"]
    },
    'muskmelon': {
        'regions': ["Western", "Northern"],
        'soil_types': ["Sandy", "Sandy Loam"],
        'growing_seasons': ["Summer", "Spring"],
        'yield_range': (12000, 25000),
        'growth_days': (85, 120),
        'irrigation': ["Drip", "Sprinkler"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (100, 180),
        'organic_matter': (1.0, 3.0),
        'crop_rotation': ["Rice", "Vegetables", "Fallow"],
        'seed_rate': (2, 3),  # kg/ha
        'market_price': (0.3, 0.6),
        'water_sources': ["Well", "Canal"]
    },
    'apple': {
        'regions': ["Northern"],
        'soil_types': ["Loamy", "Sandy Loam"],
        'growing_seasons': ["Perennial"],
        'yield_range': (15000, 30000),
        'growth_days': (1095, 1825),
        'irrigation': ["Drip", "Sprinkler"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (150, 350),
        'organic_matter': (1.5, 4.0),
        'crop_rotation': ["Fallow"],
        'seed_rate': (400, 800),  # Trees/ha
        'market_price': (0.8, 1.8),
        'water_sources': ["Well", "River", "Reservoir"]
    },
    'orange': {
        'regions': ["Southern", "Western", "Central"],
        'soil_types': ["Loamy", "Sandy Loam"],
        'growing_seasons': ["Perennial"],
        'yield_range': (12000, 25000),
        'growth_days': (730, 1460),
        'irrigation': ["Drip"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (180, 320),
        'organic_matter': (1.5, 3.8),
        'crop_rotation': ["Fallow"],
        'seed_rate': (400, 700),  # Trees/ha
        'market_price': (0.7, 1.5),
        'water_sources': ["Well", "Canal", "Reservoir"]
    },
    'papaya': {
        'regions': ["Southern", "Eastern"],
        'soil_types': ["Sandy Loam", "Loamy"],
        'growing_seasons': ["Perennial"],
        'yield_range': (20000, 40000),
        'growth_days': (270, 365),
        'irrigation': ["Drip"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["High"],
        'fertilizer_kg_ha': (200, 400),
        'organic_matter': (1.8, 4.5),
        'crop_rotation': ["Vegetables", "Fallow"],
        'seed_rate': (1800, 2500),  # Plants/ha
        'market_price': (0.5, 1.2),
        'water_sources': ["Well", "Canal"]
    },
    'coconut': {
        'regions': ["Southern"],
        'soil_types': ["Sandy", "Sandy Loam", "Loamy"],
        'growing_seasons': ["Perennial"],
        'yield_range': (10000, 20000),
        'growth_days': (1460, 1825),
        'irrigation': ["Flood", "Drip"],
        'pest_incidents': ["Low", "Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (150, 300),
        'organic_matter': (1.2, 3.5),
        'crop_rotation': ["Fallow"],
        'seed_rate': (150, 200),  # Trees/ha
        'market_price': (0.6, 1.4),
        'water_sources': ["Well", "Rain", "Canal"]
    },
    'cotton': {
        'regions': ["Western", "Central", "Southern"],
        'soil_types': ["Black", "Loamy", "Sandy Loam"],
        'growing_seasons': ["Kharif", "Monsoon"],
        'yield_range': (1500, 3500),
        'growth_days': (150, 210),
        'irrigation': ["Drip", "Flood"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (120, 250),
        'organic_matter': (1.0, 3.0),
        'crop_rotation': ["Wheat", "Pulses", "Maize"],
        'seed_rate': (15, 20),  # kg/ha
        'market_price': (1.5, 3.0),
        'water_sources': ["Well", "Canal", "Rain"]
    },
    'jute': {
        'regions': ["Eastern", "Northern"],
        'soil_types': ["Alluvial", "Loamy", "Clay Loam"],
        'growing_seasons': ["Kharif", "Monsoon"],
        'yield_range': (2000, 3500),
        'growth_days': (100, 130),
        'irrigation': ["Flood"],
        'pest_incidents': ["Low", "Medium"],
        'fertilizer_application': ["Medium"],
        'fertilizer_kg_ha': (80, 150),
        'organic_matter': (1.5, 3.5),
        'crop_rotation': ["Rice", "Pulses", "Vegetables"],
        'seed_rate': (7, 10),  # kg/ha
        'market_price': (0.8, 1.6),
        'water_sources': ["Rain", "River", "Canal"]
    },
    'coffee': {
        'regions': ["Southern", "Western"],
        'soil_types': ["Red", "Loamy", "Sandy Loam"],
        'growing_seasons': ["Perennial"],
        'yield_range': (1000, 2500),
        'growth_days': (1095, 1460),
        'irrigation': ["Drip", "Sprinkler"],
        'pest_incidents': ["Medium", "High"],
        'fertilizer_application': ["Medium", "High"],
        'fertilizer_kg_ha': (150, 300),
        'organic_matter': (2.0, 4.5),
        'crop_rotation': ["Fallow"],
        'seed_rate': (1200, 1800),  # Plants/ha
        'market_price': (2.0, 4.5),
        'water_sources': ["Well", "Rain", "Reservoir"]
    }
}

# Generate synthetic data
synthetic_data = []
for _ in range(rows_to_generate):
    # Randomly sample existing rows
    sample = data.sample(1).values[0]
    crop_label = sample[7]
    
    # Use crop-specific attributes if available, otherwise use random values
    if crop_label.lower() in crop_properties:
        properties = crop_properties[crop_label.lower()]
        region = random.choice(properties['regions'])
        soil_type = random.choice(properties['soil_types'])
        growing_season = random.choice(properties['growing_seasons'])
        yield_value = random.randint(properties['yield_range'][0], properties['yield_range'][1])
        growth_days = random.randint(properties['growth_days'][0], properties['growth_days'][1])
        irrigation_method = random.choice(properties['irrigation'])
        pest_incident = random.choice(properties['pest_incidents'])
        fertilizer_application = random.choice(properties['fertilizer_application'])
        fertilizer_kg_ha = random.randint(properties['fertilizer_kg_ha'][0], properties['fertilizer_kg_ha'][1])
        organic_matter = round(random.uniform(properties['organic_matter'][0], properties['organic_matter'][1]), 1)
        crop_rotation = random.choice(properties['crop_rotation'])
        seed_rate = random.randint(properties['seed_rate'][0], properties['seed_rate'][1])
        market_price = round(random.uniform(properties['market_price'][0], properties['market_price'][1]), 2)
        water_source = random.choice(properties['water_sources'])
    else:
        region = random.choice(regions)
        soil_type = random.choice(soil_types)
        growing_season = random.choice(growing_seasons)
        yield_value = random.randint(920, 42500)
        growth_days = random.randint(65, 1825)
        irrigation_method = random.choice(irrigation_methods)
        pest_incident = random.choice(pest_incidents)
        fertilizer_application = random.choice(fertilizer_applications)
        fertilizer_kg_ha = random.randint(20, 500)
        organic_matter = round(random.uniform(0.5, 5.0), 1)
        crop_rotation = random.choice(crop_rotation_options)
        seed_rate = random.randint(2, 2500)  # Very general range
        market_price = round(random.uniform(0.15, 8.0), 2)
        water_source = random.choice(water_sources)
    
    # Create a new row with slight variations in original columns plus new columns
    new_row = [
        sample[0] + np.random.randint(-5, 5),  # N
        sample[1] + np.random.randint(-5, 5),  # P
        sample[2] + np.random.randint(-5, 5),  # K
        sample[3] + np.random.uniform(-2, 2),  # temperature
        sample[4] + np.random.uniform(-5, 5),  # humidity
        sample[5] + np.random.uniform(-0.5, 0.5),  # ph
        sample[6] + np.random.uniform(-50, 50),  # rainfall
        sample[7],  # label
        region,  # Region
        soil_type,  # Soil Type
        growing_season,  # Growing Season
        yield_value,  # Yield
        growth_days,  # Growth Days
        irrigation_method,  # Irrigation Method
        pest_incident,  # Pest Incidents
        fertilizer_application,  # Fertilizer Application (categorical)
        fertilizer_kg_ha,  # Fertilizer kg/ha (numeric)
        organic_matter,  # Organic Matter %
        crop_rotation,  # Crop Rotation
        seed_rate,  # Seed Rate
        market_price,  # Market Price
        water_source  # Water Source
    ]
    
    synthetic_data.append(new_row)

# Create a DataFrame from the synthetic data
columns = list(data.columns) + [
    'Region', 'Soil_Type', 'Growing_Season', 'Yield_kg_per_hectare', 'Growth_Days', 
    'Irrigation_Method', 'Pest_Incidents', 'Fertilizer_Application', 'Fertilizer_kg_ha',
    'Organic_Matter_Percentage', 'Crop_Rotation', 'Seed_Rate_kg_ha', 'Market_Price_USD_per_kg',
    'Water_Source'
]
synthetic_df = pd.DataFrame(synthetic_data, columns=columns)

# Ensure all numeric values are within reasonable bounds
for col, (min_val, max_val) in zip(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'], 
                                   [(0, 200), (5, 200), (5, 200), (0, 50), (0, 100), (0, 14), (0, 400)]):
    synthetic_df[col] = synthetic_df[col].clip(min_val, max_val)

# Combine original data with new columns (for original data, populate with reasonable values)
for new_col in [
    'Region', 'Soil_Type', 'Growing_Season', 'Yield_kg_per_hectare', 'Growth_Days', 
    'Irrigation_Method', 'Pest_Incidents', 'Fertilizer_Application', 'Fertilizer_kg_ha',
    'Organic_Matter_Percentage', 'Crop_Rotation', 'Seed_Rate_kg_ha', 'Market_Price_USD_per_kg',
    'Water_Source'
]:
    if new_col not in data.columns:
        data[new_col] = None  # Initialize columns that will be filled

# Fill in the new columns for original data based on crop type
for idx, row in data.iterrows():
    crop = row['label'].lower()
    if crop in crop_properties:
        properties = crop_properties[crop]
        data.at[idx, 'Region'] = random.choice(properties['regions'])
        data.at[idx, 'Soil_Type'] = random.choice(properties['soil_types'])
        data.at[idx, 'Growing_Season'] = random.choice(properties['growing_seasons'])
        data.at[idx, 'Yield_kg_per_hectare'] = random.randint(properties['yield_range'][0], properties['yield_range'][1])
        data.at[idx, 'Growth_Days'] = random.randint(properties['growth_days'][0], properties['growth_days'][1])
        data.at[idx, 'Irrigation_Method'] = random.choice(properties['irrigation'])
        data.at[idx, 'Pest_Incidents'] = random.choice(properties['pest_incidents'])
        data.at[idx, 'Fertilizer_Application'] = random.choice(properties['fertilizer_application'])
        data.at[idx, 'Fertilizer_kg_ha'] = random.randint(properties['fertilizer_kg_ha'][0], properties['fertilizer_kg_ha'][1])
        data.at[idx, 'Organic_Matter_Percentage'] = round(random.uniform(properties['organic_matter'][0], properties['organic_matter'][1]), 1)
        data.at[idx, 'Crop_Rotation'] = random.choice(properties['crop_rotation'])
        data.at[idx, 'Seed_Rate_kg_ha'] = random.randint(properties['seed_rate'][0], properties['seed_rate'][1])
        data.at[idx, 'Market_Price_USD_per_kg'] = round(random.uniform(properties['market_price'][0], properties['market_price'][1]), 2)
        data.at[idx, 'Water_Source'] = random.choice(properties['water_sources'])
    else:
        data.at[idx, 'Region'] = random.choice(regions)
        data.at[idx, 'Soil_Type'] = random.choice(soil_types)
        data.at[idx, 'Growing_Season'] = random.choice(growing_seasons)
        data.at[idx, 'Yield_kg_per_hectare'] = random.randint(920, 42500)
        data.at[idx, 'Growth_Days'] = random.randint(65, 1825)
        data.at[idx, 'Irrigation_Method'] = random.choice(irrigation_methods)
        data.at[idx, 'Pest_Incidents'] = random.choice(pest_incidents)
        data.at[idx, 'Fertilizer_Application'] = random.choice(fertilizer_applications)
        data.at[idx, 'Fertilizer_kg_ha'] = random.randint(20, 500)
        data.at[idx, 'Organic_Matter_Percentage'] = round(random.uniform(0.5, 5.0), 1)
        data.at[idx, 'Crop_Rotation'] = random.choice(crop_rotation_options)
        data.at[idx, 'Seed_Rate_kg_ha'] = random.randint(2, 2500)
        data.at[idx, 'Market_Price_USD_per_kg'] = round(random.uniform(0.15, 8.0), 2)
        data.at[idx, 'Water_Source'] = random.choice(water_sources)

# Combine original and synthetic data
final_data = pd.concat([data, synthetic_df], ignore_index=True)

# Save the final combined dataset
final_data.to_csv('dataset/Crop_recommendation_extended.csv', index=False)

print(f"Successfully generated {rows_to_generate} new rows with added columns.")
print(f"Total dataset size: {len(final_data)} rows")
print(f"New columns added: Region, Soil_Type, Growing_Season, Yield_kg_per_hectare, Growth_Days, Irrigation_Method, Pest_Incidents, Fertilizer_Application, Fertilizer_kg_ha, Organic_Matter_Percentage, Crop_Rotation, Seed_Rate_kg_ha, Market_Price_USD_per_kg, Water_Source")