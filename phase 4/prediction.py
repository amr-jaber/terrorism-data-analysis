import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import warnings

# Ignore unnecessary warnings
warnings.filterwarnings("ignore")

# 1. Load Data
path = r'E:\level 3\2\lab\python-mohamed\terrorism attack expecting\globalterrorismdb_0718dist.csv'
df = pd.read_csv(path, usecols=['attacktype1_txt', 'nkill'], low_memory=False, encoding='ISO-8859-1')

# 2. Data Cleaning
df['nkill'] = pd.to_numeric(df['nkill'], errors='coerce').fillna(0)
df = df[df['attacktype1_txt'] != 'Unknown']

# 3. Encoding Label
le = LabelEncoder()
df['attack_type_code'] = le.fit_transform(df['attacktype1_txt'])

# 4. Training the Model
X = df[['attack_type_code']] 
y = df['nkill']
model = LinearRegression()
model.fit(X, y)

# 5. Output Prediction Results
print("-" * 60)
print(f"{'Attack Type':<25} | {'Predicted Fatalities':<20}")
print("-" * 60)

sample_types = ['Assassination', 'Bombing/Explosion', 'Armed Assault']

for name in sample_types:
    code = le.transform([name])[0]
    input_data = pd.DataFrame([[code]], columns=['attack_type_code'])
    prediction = model.predict(input_data)
    # Ensure prediction is not negative and round it
    final_pred = round(max(0, prediction[0]), 2)
    print(f"{name:<25} | {final_pred:<20}")

print("-" * 60)
print("Prediction completed successfully.")