import tkinter as tk
from tkinter import ttk
import random
import math

class GreenhouseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление микроклиматом в теплице")
        self.geometry("600x500")
        self.resizable(False, False)

        # --- Параметры симуляции ---
        self.temperature = 22.0          # текущая температура
        self.humidity = 60.0              # текущая влажность
        self.light = 500.0                 # текущая освещённость (усл. ед.)
        self.target_temp = 22.0            # целевая температура
        self.target_humidity = 60.0        # целевая влажность

        # Состояния устройств (вкл/выкл)
        self.heater_on = False
        self.fan_on = False
        self.pump_on = False
        self.light_on = False

        # Режим: "manual" или "auto"
        self.mode = tk.StringVar(value="manual")

        # --- Создание элементов интерфейса ---
        self.create_widgets()

        # Запуск цикла обновления симуляции
        self.update_simulation()

    def create_widgets(self):
        # ---- Стили ----
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        style.configure("Value.TLabel", font=("Arial", 20, "bold"), foreground="darkblue")

        # ---- Текущие показания (фрейм) ----
        frame_current = ttk.LabelFrame(self, text="Текущие показания", padding=10)
        frame_current.pack(fill="x", padx=10, pady=5)

        # Температура
        ttk.Label(frame_current, text="Температура:", style="Header.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        self.lbl_temp = ttk.Label(frame_current, text=f"{self.temperature:.1f} °C", style="Value.TLabel")
        self.lbl_temp.grid(row=0, column=1, padx=5)

        # Влажность
        ttk.Label(frame_current, text="Влажность:", style="Header.TLabel").grid(row=1, column=0, sticky="w", padx=5)
        self.lbl_humidity = ttk.Label(frame_current, text=f"{self.humidity:.1f} %", style="Value.TLabel")
        self.lbl_humidity.grid(row=1, column=1, padx=5)

        # Освещённость
        ttk.Label(frame_current, text="Освещённость:", style="Header.TLabel").grid(row=2, column=0, sticky="w", padx=5)
        self.lbl_light = ttk.Label(frame_current, text=f"{self.light:.0f} lx", style="Value.TLabel")
        self.lbl_light.grid(row=2, column=1, padx=5)

        # ---- Целевые параметры ----
        frame_target = ttk.LabelFrame(self, text="Целевые параметры", padding=10)
        frame_target.pack(fill="x", padx=10, pady=5)

        # Целевая температура
        ttk.Label(frame_target, text="Температура (°C):").grid(row=0, column=0, sticky="w")
        self.target_temp_var = tk.DoubleVar(value=self.target_temp)
        self.target_temp_slider = ttk.Scale(frame_target, from_=10, to=35, orient="horizontal",
                                            variable=self.target_temp_var, command=self.on_target_temp_change)
        self.target_temp_slider.grid(row=0, column=1, padx=5, sticky="ew")
        self.lbl_target_temp = ttk.Label(frame_target, text=f"{self.target_temp:.1f}")
        self.lbl_target_temp.grid(row=0, column=2, padx=5)

        # Целевая влажность
        ttk.Label(frame_target, text="Влажность (%):").grid(row=1, column=0, sticky="w")
        self.target_humidity_var = tk.DoubleVar(value=self.target_humidity)
        self.target_humidity_slider = ttk.Scale(frame_target, from_=30, to=90, orient="horizontal",
                                                variable=self.target_humidity_var, command=self.on_target_humidity_change)
        self.target_humidity_slider.grid(row=1, column=1, padx=5, sticky="ew")
        self.lbl_target_humidity = ttk.Label(frame_target, text=f"{self.target_humidity:.1f}")
        self.lbl_target_humidity.grid(row=1, column=2, padx=5)

        frame_target.columnconfigure(1, weight=1)

        # ---- Управление устройствами ----
        frame_control = ttk.LabelFrame(self, text="Управление устройствами", padding=10)
        frame_control.pack(fill="x", padx=10, pady=5)

        # Обогреватель
        self.btn_heater = tk.Button(frame_control, text="Обогреватель", width=15, bg="lightgray",
                                    command=self.toggle_heater)
        self.btn_heater.grid(row=0, column=0, padx=5, pady=5)

        # Вентилятор
        self.btn_fan = tk.Button(frame_control, text="Вентилятор", width=15, bg="lightgray",
                                 command=self.toggle_fan)
        self.btn_fan.grid(row=0, column=1, padx=5, pady=5)

        # Насос (полив)
        self.btn_pump = tk.Button(frame_control, text="Насос", width=15, bg="lightgray",
                                  command=self.toggle_pump)
        self.btn_pump.grid(row=1, column=0, padx=5, pady=5)

        # Освещение
        self.btn_light = tk.Button(frame_control, text="Освещение", width=15, bg="lightgray",
                                   command=self.toggle_light)
        self.btn_light.grid(row=1, column=1, padx=5, pady=5)

        # ---- Режим работы ----
        frame_mode = ttk.LabelFrame(self, text="Режим работы", padding=10)
        frame_mode.pack(fill="x", padx=10, pady=5)

        ttk.Radiobutton(frame_mode, text="Ручной", variable=self.mode, value="manual").pack(side="left", padx=5)
        ttk.Radiobutton(frame_mode, text="Автомат", variable=self.mode, value="auto").pack(side="left", padx=5)

        # ---- Информация ----
        self.lbl_info = ttk.Label(self, text="", font=("Arial", 10))
        self.lbl_info.pack(pady=5)

    # ---- Обработчики ползунков целевых значений ----
    def on_target_temp_change(self, event=None):
        self.target_temp = self.target_temp_var.get()
        self.lbl_target_temp.config(text=f"{self.target_temp:.1f}")

    def on_target_humidity_change(self, event=None):
        self.target_humidity = self.target_humidity_var.get()
        self.lbl_target_humidity.config(text=f"{self.target_humidity:.1f}")

    # ---- Переключение устройств (ручное) ----
    def toggle_heater(self):
        if self.mode.get() == "manual":
            self.heater_on = not self.heater_on
            self.update_button_color(self.btn_heater, self.heater_on)

    def toggle_fan(self):
        if self.mode.get() == "manual":
            self.fan_on = not self.fan_on
            self.update_button_color(self.btn_fan, self.fan_on)

    def toggle_pump(self):
        if self.mode.get() == "manual":
            self.pump_on = not self.pump_on
            self.update_button_color(self.btn_pump, self.pump_on)

    def toggle_light(self):
        if self.mode.get() == "manual":
            self.light_on = not self.light_on
            self.update_button_color(self.btn_light, self.light_on)

    def update_button_color(self, button, state):
        button.config(bg="lightgreen" if state else "lightgray")

    # ---- Автоматическое регулирование ----
    def auto_control(self):
        if self.mode.get() == "auto":
            # Регулирование температуры
            if self.temperature < self.target_temp - 0.5:
                if not self.heater_on:
                    self.heater_on = True
                    self.update_button_color(self.btn_heater, True)
            elif self.temperature > self.target_temp + 0.5:
                if not self.fan_on:
                    self.fan_on = True
                    self.update_button_color(self.btn_fan, True)
            else:
                if self.heater_on:
                    self.heater_on = False
                    self.update_button_color(self.btn_heater, False)
                if self.fan_on:
                    self.fan_on = False
                    self.update_button_color(self.btn_fan, False)

            # Регулирование влажности (простой пример: если влажность ниже целевой, включаем насос)
            if self.humidity < self.target_humidity - 2:
                if not self.pump_on:
                    self.pump_on = True
                    self.update_button_color(self.btn_pump, True)
            elif self.humidity > self.target_humidity + 2:
                if self.pump_on:
                    self.pump_on = False
                    self.update_button_color(self.btn_pump, False)

            # Освещение – если значение освещённости упадёт ниже порога (ночная имитация)
            if self.light < 300:
                if not self.light_on:
                    self.light_on = True
                    self.update_button_color(self.btn_light, True)
            else:
                if self.light_on:
                    self.light_on = False
                    self.update_button_color(self.btn_light, False)

    # ---- Симуляция изменения параметров ----
    def simulate_environment(self):
        # Влияние устройств
        if self.heater_on:
            self.temperature += 0.2
        if self.fan_on:
            self.temperature -= 0.15
            self.humidity -= 0.1   # вентилятор слегка сушит воздух
        if self.pump_on:
            self.humidity += 0.5
        if self.light_on:
            self.light += 20        # освещение увеличивает освещённость
            self.temperature += 0.05 # лампы немного греют
        else:
            # естественное снижение освещённости (имитация дня/ночи – простейшая)
            self.light -= 10

        # Случайные флуктуации
        self.temperature += random.uniform(-0.1, 0.1)
        self.humidity += random.uniform(-0.2, 0.2)
        self.light += random.uniform(-5, 5)

        # Ограничения
        self.temperature = max(5, min(45, self.temperature))
        self.humidity = max(20, min(100, self.humidity))
        self.light = max(0, min(1000, self.light))

    def update_display(self):
        self.lbl_temp.config(text=f"{self.temperature:.1f} °C")
        self.lbl_humidity.config(text=f"{self.humidity:.1f} %")
        self.lbl_light.config(text=f"{self.light:.0f} lx")

    def update_simulation(self):
        self.auto_control()
        self.simulate_environment()
        self.update_display()
        # Планируем следующее обновление через 1000 мс (1 секунда)
        self.after(1000, self.update_simulation)

if __name__ == "__main__":
    app = GreenhouseApp()
    app.mainloop()