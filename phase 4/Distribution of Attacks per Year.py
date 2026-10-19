import pandas as pd
import matplotlib.pyplot as plt

# مسار الملف الأساسي
path = r'E:\level 3\2\lab\python-mohamed\terrorism attack expecting\globalterrorismdb_0718dist.csv'

# قراءة الأعمدة المطلوبة فقط للسرعة
df = pd.read_csv(path, usecols=['iyear'], low_memory=False, encoding='ISO-8859-1')

# إعداد الرسمة (مقاس وسط)
plt.figure(figsize=(10, 5))

# حساب عدد الحوادث لكل سنة ورسمها كأعمدة
yearly_counts = df['iyear'].value_counts().sort_index()
yearly_counts.plot(kind='bar', color='skyblue', width=0.8)

# العناوين
plt.title('Distribution of Terrorist Attacks per Year (1970-2017)')
plt.xlabel('Year ()')
plt.ylabel('Number of Attacks ()')

# تدوير السنوات تحت عشان تبان بوضوح
plt.xticks(rotation=90, fontsize=8)

plt.tight_layout()
plt.show()