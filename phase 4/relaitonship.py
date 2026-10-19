import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# مسار الملف الأساسي
path = r'E:\level 3\2\lab\python-mohamed\terrorism attack expecting\globalterrorismdb_0718dist.csv'

# قراءة نوع الهجوم وعدد القتلى
df = pd.read_csv(path, usecols=['attacktype1_txt', 'nkill'], low_memory=False, encoding='ISO-8859-1')

# تنظيف البيانات: تحويل القتلى لأرقام وحذف الأنواع غير المعروفة
df['nkill'] = pd.to_numeric(df['nkill'], errors='coerce').fillna(0)
df_filtered = df[(df['attacktype1_txt'] != 'Unknown') & (df['nkill'] > 0)]

# إعداد الرسمة (مقاس وسط)
plt.figure(figsize=(10, 6))

# رسم العلاقة باستخدام المتوسط (Mean)
sns.barplot(x='attacktype1_txt', y='nkill', data=df_filtered, estimator='mean', errorbar=None, palette='rocket')

# العناوين
plt.title('Relationship: Attack Type vs Average Deaths per Incident')
plt.xlabel('Attack Type (نوع الهجوم)')
plt.ylabel('Average Deaths (متوسط القتلى في الهجوم الواحد)')

# تدوير الكلمات عشان ما تتداخل
plt.xticks(rotation=45, ha='right', fontsize=10)

plt.tight_layout()
plt.show()