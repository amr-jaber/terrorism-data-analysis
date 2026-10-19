import pandas as pd
import numpy as np

# مسار ملف البيانات بعد معالجة القيم المفقودة
input_path = r"E:\level 3\2\lab\python-mohamed\terrorism attack expecting\phase 3\معالجة القيم المفقودة\data.csv"

# مسار حفظ الناتج
output_path = r"E:\level 3\2\lab\python-mohamed\terrorism attack expecting\phase 3\التعامل مع القيم المتطرفة\outliers_cleaned.csv"

print("📌 قراءة البيانات...")
df = pd.read_csv(input_path)

print("شكل البيانات:", df.shape)

# اختيار الأعمدة الرقمية فقط
num_cols = df.select_dtypes(include=np.number).columns

print("\n📌 معالجة القيم المتطرفة باستخدام IQR...")

for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df[col] = np.where(df[col] < lower, lower, df[col])
    df[col] = np.where(df[col] > upper, upper, df[col])

print("✅ تم معالجة القيم المتطرفة")

# حفظ الملف
df.to_csv(output_path, index=False)

print("\n📁 تم حفظ الملف في:")
print(output_path)

print("\n📌 أول 5 صفوف:")
print(df.head())
