import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load and Prepare Data
path = r'E:\level 3\2\lab\python-mohamed\terrorism attack expecting\globalterrorismdb_0718dist.csv'
df = pd.read_csv(path, usecols=['attacktype1_txt', 'nkill'], low_memory=False, encoding='ISO-8859-1')
df['nkill'] = pd.to_numeric(df['nkill'], errors='coerce').fillna(0)

# Convert categorical data to numbers
df = pd.get_dummies(df, columns=['attacktype1_txt'])

# 2. Split Data (80% Training, 20% Testing)
X = df.drop('nkill', axis=1)
y = df['nkill']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Define Algorithms
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(max_depth=5),
    "Random Forest": RandomForestRegressor(n_estimators=10, max_depth=5)
}

# 4. Training and Evaluation
print("-" * 65)
print(f"{'Algorithm':<25} | {'MAE (Error)':<15} | {'R2 Score':<15}")
print("-" * 65)

for name, model in models.items():
    model.fit(X_train, y_train)  # Train
    preds = model.predict(X_test) # Test
    
    mae = mean_absolute_error(y_test, preds) # Mean Absolute Error
    r2 = r2_score(y_test, preds)             # Accuracy Score
    
    print(f"{name:<25} | {mae:<15.4f} | {r2:<15.4f}")

print("-" * 65)
print("Phase 5: Model Training and Comparison Completed.")