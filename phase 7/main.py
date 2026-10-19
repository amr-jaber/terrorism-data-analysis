import tkinter as tk
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import warnings

# تجاهل التحذيرات
warnings.filterwarnings("ignore")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TerrorismApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Global Terrorism Analysis Dashboard - 2026")
        self.geometry("1300x850")

        # المسار الأساسي (الرسمي)
        self.csv_path = r'E:\level 3\2\lab\python-mohamed\terrorism attack expecting\globalterrorismdb_0718dist.csv'
        self.custom_file_path = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- القائمة الجانبية ---
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Main Menu", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=(20, 10), padx=20)

        # أزرار الكود الرسمي (تم إصلاحها بالكامل)
        self.create_sidebar_button("Attack Distribution", self.run_distribution)
        self.create_sidebar_button("Attacks Relationship", self.run_relationship)
        self.create_sidebar_button("Fatality Prediction", self.run_prediction)
        self.create_sidebar_button("Model Comparison", self.run_comparison, color="#2E7D32")
        
        # --- مربع اختيار ملف جديد ---
        self.upload_frame = ctk.CTkFrame(self.sidebar, corner_radius=15, fg_color="#2b2b2b", border_width=1, border_color="#3d3d3d")
        self.upload_frame.pack(pady=15, padx=15, fill="x")

        self.btn_browse = ctk.CTkButton(self.upload_frame, text="📁 Select Database File", 
                                        command=self.browse_custom_file, fg_color="#3b3b3b", hover_color="#4b4b4b")
        self.btn_browse.pack(pady=(10, 5), padx=10)

        self.file_status_label = ctk.CTkLabel(self.upload_frame, text="No custom file", font=("Arial", 11), text_color="gray")
        self.file_status_label.pack(pady=2)

        self.custom_actions_frame = ctk.CTkFrame(self.upload_frame, fg_color="transparent")

        # --- ComboBox الإحصائيات ---
        self.stats_label = ctk.CTkLabel(self.sidebar, text="Quick Statistics Box", font=("Arial", 12, "bold"))
        self.stats_label.pack(pady=(15, 5))
        
        self.stats_combo = ctk.CTkComboBox(self.sidebar, 
                                           values=["Select Statistic", "Total Fatalities (Kill)", "Total Wounded", "Suicide Attacks", "Top Targeted Country"],
                                           command=self.show_quick_stats)
        self.stats_combo.pack(pady=10, padx=20, fill="x")

        self.spacer = ctk.CTkLabel(self.sidebar, text="")
        self.spacer.pack(expand=True)

        # زر دليل الاستخدام
        self.btn_help = ctk.CTkButton(self.sidebar, text="User Guide (?)", fg_color="#555555", hover_color="#777777", command=self.show_user_guide)
        self.btn_help.pack(pady=20, padx=20, fill="x")

        # --- منطقة العرض ---
        self.main_view = ctk.CTkFrame(self, corner_radius=15)
        self.main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.canvas_frame = ctk.CTkFrame(self.main_view, fg_color="#1a1a1a", corner_radius=10)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.result_text = ctk.CTkTextbox(self.main_view, height=180, font=("Consolas", 13), border_width=2)
        self.result_text.pack(fill="x", padx=20, pady=(0, 20))

        self.canvas = None
        self.display_welcome()

    def create_sidebar_button(self, text, command, color=None):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, fg_color=color, height=35)
        btn.pack(pady=8, padx=20, fill="x")

    def clear_view(self):
        if self.canvas: self.canvas.get_tk_widget().destroy()
        self.result_text.delete("1.0", tk.END)
        plt.close('all')

    def display_plot(self, fig):
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def display_welcome(self):
        self.result_text.insert("0.0", "Welcome! Dashboard is ready. All primary buttons are fully functional.")

    # --- تم إصلاح الأزرار هنا (إعادة كتابة المحركات بالكامل) ---

    def run_prediction(self):
        self.clear_view()
        try:
            df = pd.read_csv(self.csv_path, usecols=['attacktype1_txt', 'nkill'], low_memory=False, encoding='ISO-8859-1')
            df['nkill'] = pd.to_numeric(df['nkill'], errors='coerce').fillna(0)
            df = df[df['attacktype1_txt'] != 'Unknown']
            
            le = LabelEncoder()
            df['attack_type_code'] = le.fit_transform(df['attacktype1_txt'])
            
            X, y = df[['attack_type_code']], df['nkill']
            model = LinearRegression().fit(X, y)

            res = f"{'Attack Type':<25} | {'Predicted Fatalities':<20}\n" + "-"*55 + "\n"
            samples = ['Assassination', 'Bombing/Explosion', 'Armed Assault']
            names, vals = [], []
            for name in samples:
                code = le.transform([name])[0]
                p = max(0, model.predict([[code]])[0])
                res += f"{name:<25} | {round(p, 2):<20}\n"
                names.append(name); vals.append(p)
            
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(names, vals, color=['#3498db', '#e74c3c', '#2ecc71'])
            ax.set_title("Linear Regression: Fatality Prediction")
            self.display_plot(fig)
            self.result_text.insert("end", res + "\nPrediction Phase Completed.")
        except Exception as e: self.result_text.insert("end", f"Prediction Error: {str(e)}")

    def run_comparison(self):
        self.clear_view()
        self.result_text.insert("end", "Training ML Models... Please wait (this takes a few seconds)\n")
        self.update()
        try:
            df = pd.read_csv(self.csv_path, usecols=['attacktype1_txt', 'nkill'], low_memory=False, encoding='ISO-8859-1')
            df['nkill'] = pd.to_numeric(df['nkill'], errors='coerce').fillna(0)
            df = pd.get_dummies(df, columns=['attacktype1_txt'])
            
            X, y = df.drop('nkill', axis=1), df['nkill']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(max_depth=5),
                "Random Forest": RandomForestRegressor(n_estimators=10, max_depth=5)
            }

            res = f"{'Algorithm':<20} | {'MAE':<10} | {'R2 Score':<10}\n" + "-"*50 + "\n"
            names, r2_scores = [], []
            for n, m in models.items():
                m.fit(X_train, y_train)
                preds = m.predict(X_test)
                mae = mean_absolute_error(y_test, preds)
                r2 = r2_score(y_test, preds)
                res += f"{n:<20} | {mae:<10.3f} | {r2:<10.3f}\n"
                names.append(n); r2_scores.append(r2)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.barh(names, r2_scores, color='teal')
            ax.set_title("Model Accuracy Comparison (R2)")
            self.display_plot(fig)
            self.result_text.insert("end", res)
        except Exception as e: self.result_text.insert("end", f"Comparison Error: {str(e)}")

    # --- بقية الدوال (التوزيع، العلاقة، الإحصائيات) ---

    def run_distribution(self, path=None):
        target = path if path else self.csv_path
        self.clear_view()
        try:
            df = pd.read_csv(target, usecols=['iyear'], low_memory=False, encoding='ISO-8859-1')
            fig, ax = plt.subplots(figsize=(10, 5))
            df['iyear'].value_counts().sort_index().plot(kind='bar', color='skyblue', ax=ax)
            ax.set_title('Distribution of Attacks per Year')
            plt.xticks(rotation=90, fontsize=8); plt.tight_layout()
            self.display_plot(fig)
            self.result_text.insert("end", f"Data Loaded Successfully from: {target.split('/')[-1]}")
        except Exception as e: self.result_text.insert("end", str(e))

    def run_relationship(self, path=None):
        target = path if path else self.csv_path
        self.clear_view()
        try:
            df = pd.read_csv(target, usecols=['attacktype1_txt', 'nkill'], low_memory=False, encoding='ISO-8859-1')
            df['nkill'] = pd.to_numeric(df['nkill'], errors='coerce').fillna(0)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='attacktype1_txt', y='nkill', data=df, estimator='mean', errorbar=None, palette='rocket', ax=ax)
            plt.xticks(rotation=45, ha='right'); plt.tight_layout()
            self.display_plot(fig)
        except Exception as e: self.result_text.insert("end", str(e))

    def show_quick_stats(self, choice):
        if choice == "Select Statistic": return
        self.clear_view()
        try:
            df = pd.read_csv(self.csv_path, usecols=['nkill', 'nwound', 'suicide', 'country_txt'], low_memory=False, encoding='ISO-8859-1')
            total = len(df)
            msg = f"--- Statistical Report: {choice} ---\n\n"
            if choice == "Total Fatalities (Kill)":
                val = df['nkill'].sum()
                msg += f"Total: {int(val):,}\nAvg per Attack: {df['nkill'].mean():.2f}"
            elif choice == "Total Wounded":
                val = df['nwound'].sum()
                msg += f"Total: {int(val):,}\nImpact Ratio: {(val/total)*100:.2f}%"
            elif choice == "Suicide Attacks":
                val = df['suicide'].sum()
                msg += f"Count: {int(val):,}\nPercentage: {(val/total)*100:.2f}%"
            elif choice == "Top Targeted Country":
                top = df['country_txt'].value_counts()
                msg += f"Country: {top.idxmax()}\nAttacks: {top.max():,}\nGlobal Share: {(top.max()/total)*100:.2f}%"
            self.result_text.insert("0.0", msg)
        except Exception as e: self.result_text.insert("end", str(e))

    def browse_custom_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.custom_file_path = path
            self.file_status_label.configure(text=f"✅ Loaded: {path.split('/')[-1]}", text_color="#4CAF50")
            self.show_custom_buttons()

    def show_custom_buttons(self):
        for widget in self.custom_actions_frame.winfo_children(): widget.destroy()
        self.custom_actions_frame.pack(pady=10, fill="x")
        ctk.CTkButton(self.custom_actions_frame, text="Custom Dist", command=lambda: self.run_distribution(self.custom_file_path)).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self.custom_actions_frame, text="Custom Rel", command=lambda: self.run_relationship(self.custom_file_path)).pack(pady=5, padx=10, fill="x")

    def show_user_guide(self):
        guide_window = ctk.CTkToplevel(self)
        guide_window.title("User Guide - دليل الاستخدام")
        guide_window.geometry("600x500")
        guide_window.attributes("-topmost", True)
        
        # صندوق النص
        txt = ctk.CTkTextbox(guide_window, width=580, height=480, font=("Arial", 14))
        txt.pack(padx=10, pady=10)
        
        # النص العربي مع المصطلحات الإنجليزية
        guide_text = (
            "=== دليل استخدام نظام التحليل 2026 ===\n\n"
            "1. أزرار القائمة الجانبية (Sidebar buttons):\n"
            "   - [Attack Distribution]: تحليل توزيع الهجمات سنوياً.\n"
            "   - [Attacks Relationship]: تحليل العلاقة بين نوع الهجوم والضحايا.\n"
            "   - [Fatality Prediction]: التنبؤ بالضحايا باستخدام الذكاء الاصطناعي.\n"
            "   - [Model Comparison]: مقارنة دقة خوارزميات التعلم الآلي.\n\n"
            "2. صندوق الإحصائيات (ComboBox):\n"
            "   - يقدم إحصائيات رقمية سريعة (Quick numeric stats) تشمل إجمالي القتلى، "
            "الجرحى، والعمليات الانتحارية مع حساب النسبة المئوية (%) لكل منها.\n\n"
            "3. الملف المندرج (Custom File):\n"
            "   - من خلال زر [Select Database File] يمكنك رفع ملف CSV خاص بك "
            "وتحليله بشكل مستقل عبر أزرار التحليل المخصصة التي ستظهر فوراً.\n\n"
            "4. عرض النتائج:\n"
            "   - الرسوم البيانية تظهر في اللوحة المركزية، بينما التفاصيل الرقمية "
            "تظهر في صندوق النصوص السفلي [Result Text]."
        )
        
        txt.insert("0.0", guide_text)
        txt.configure(state="disabled")

if __name__ == "__main__":
    app = TerrorismApp(); app.mainloop()