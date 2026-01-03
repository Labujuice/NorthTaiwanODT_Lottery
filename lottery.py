import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
import time
import datetime
import webbrowser
import threading

CSV_FILE = "attractions.csv"
LOG_FILE = "lottery_history.csv"

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("北台灣一日遊景點抽籤")
        self.root.geometry("600x500")

        self.attractions = []
        self.load_data()

        # UI Components
        self.create_widgets()
        
        # Determine unique filter values
        self.update_filter_options()

    def load_data(self):
        try:
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.attractions = list(reader)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load {CSV_FILE}\n{e}")
            self.attractions = []

    def create_widgets(self):
        # Title
        title_lbl = tk.Label(self.root, text="🎰 北台灣一日遊抽籤 🎰", font=("Arial", 24, "bold"))
        title_lbl.pack(pady=10)

        # Filters Frame
        filter_frame = tk.LabelFrame(self.root, text="篩選條件", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=20)

        # Region
        tk.Label(filter_frame, text="縣市:").grid(row=0, column=0, padx=5, sticky="e")
        self.region_var = tk.StringVar(value="All")
        self.region_cb = ttk.Combobox(filter_frame, textvariable=self.region_var, state="readonly")
        self.region_cb.grid(row=0, column=1, padx=5, pady=5)

        # Cost
        tk.Label(filter_frame, text="費用:").grid(row=0, column=2, padx=5, sticky="e")
        self.cost_var = tk.StringVar(value="All")
        self.cost_cb = ttk.Combobox(filter_frame, textvariable=self.cost_var, state="readonly")
        self.cost_cb.grid(row=0, column=3, padx=5, pady=5)

        # Age
        tk.Label(filter_frame, text="年齡層:").grid(row=0, column=4, padx=5, sticky="e")
        self.age_var = tk.StringVar(value="All")
        self.age_cb = ttk.Combobox(filter_frame, textvariable=self.age_var, state="readonly")
        self.age_cb.grid(row=0, column=5, padx=5, pady=5)

        # Start Button
        self.start_btn = tk.Button(self.root, text="開始抽籤!", bg="#4CAF50", fg="white", font=("Arial", 16, "bold"), command=self.start_lottery)
        self.start_btn.pack(pady=20, ipadx=20, ipady=10)

        # Result Display with Lottery Animation
        self.result_frame = tk.Frame(self.root, relief="ridge", borderwidth=4)
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.result_label = tk.Label(self.result_frame, text="準備好了嗎？", font=("Arial", 28, "bold"), fg="#333", wraplength=550)
        self.result_label.pack(expand=True)
        
        self.details_label = tk.Label(self.result_frame, text="", font=("Arial", 12))
        self.details_label.pack(pady=5)

        self.link_btn = tk.Button(self.result_frame, text="查看地圖", state="disabled", command=self.open_map)
        self.link_btn.pack(pady=10)

        self.current_map_link = ""
        self.is_spinning = False

        # Logs Button (Optional, simple popup)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", pady=5)
        hist_btn = tk.Button(btn_frame, text="查看歷史紀錄", command=self.show_history)
        hist_btn.pack(side="right", padx=20)

    def update_filter_options(self):
        regions = set()
        costs = set()
        ages = set()

        for item in self.attractions:
            regions.add(item['縣市'])
            costs.add(item['費用'])
            # Ages logic might need splitting if multiple supported, but data seems simple (one value)
            if item['年齡層']:
                ages.add(item['年齡層'])

        self.region_cb['values'] = ["All"] + sorted(list(regions))
        self.cost_cb['values'] = ["All"] + sorted(list(costs))
        self.age_cb['values'] = ["All"] + sorted(list(ages))

        self.region_cb.current(0)
        self.cost_cb.current(0)
        self.age_cb.current(0)

    def get_filtered_candidates(self):
        candidates = []
        r_filter = self.region_var.get()
        c_filter = self.cost_var.get()
        a_filter = self.age_var.get()

        for item in self.attractions:
            if r_filter != "All" and r_filter not in item['縣市']:
                continue
            if c_filter != "All" and c_filter not in item['費用']:
                continue
            if a_filter != "All" and a_filter not in item['年齡層']:
                continue
            candidates.append(item)
        return candidates

    def start_lottery(self):
        if self.is_spinning:
            return

        candidates = self.get_filtered_candidates()
        if not candidates:
            messagebox.showinfo("提示", "沒有符合條件的景點！")
            return

        self.is_spinning = True
        self.start_btn.config(state="disabled")
        self.link_btn.config(state="disabled", text="查看地圖")
        self.details_label.config(text="")

        # Start animation in a separate thread so UI doesn't freeze
        threading.Thread(target=self.run_animation, args=(candidates,), daemon=True).start()

    def run_animation(self, candidates):
        # Animation loop
        duration = 3.0  # seconds
        start_time = time.time()
        delay = 0.05
        
        final_choice = None
        
        while time.time() - start_time < duration:
            temp_choice = random.choice(candidates)
            self.update_ui_text(temp_choice['景點名稱'])
            time.sleep(delay)
            # Slow down gradually
            if time.time() - start_time > duration * 0.7:
                delay += 0.05

        final_choice = random.choice(candidates)
        self.update_ui_text(final_choice['景點名稱'])
        
        self.root.after(0, self.finalize_result, final_choice)

    def update_ui_text(self, text):
        self.result_label.config(text=text)

    def finalize_result(self, choice):
        self.is_spinning = False
        self.start_btn.config(state="normal")
        
        self.current_map_link = choice['Google地圖連結']
        self.link_btn.config(state="normal")
        
        details = f"📍 {choice['縣市']} | 💰 {choice['費用']} | 👥 {choice['年齡層']}"
        self.details_label.config(text=details)
        
        self.save_log(choice)

    def open_map(self):
        if self.current_map_link:
            webbrowser.open(self.current_map_link)

    def save_log(self, choice):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_exists = False
        try:
            with open(LOG_FILE, 'r') as f:
                file_exists = True
        except FileNotFoundError:
            pass

        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Name", "City", "Cost", "Age"])
            writer.writerow([timestamp, choice['景點名稱'], choice['縣市'], choice['費用'], choice['年齡層']])

    def show_history(self):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Simple popup window for history
            top = tk.Toplevel(self.root)
            top.title("歷史紀錄")
            top.geometry("500x400")
            
            txt = tk.Text(top, wrap="none")
            txt.pack(fill="both", expand=True)
            txt.insert("1.0", content)
            txt.config(state="disabled")
            
        except FileNotFoundError:
            messagebox.showinfo("Info", "目前沒有歷史紀錄")

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()
