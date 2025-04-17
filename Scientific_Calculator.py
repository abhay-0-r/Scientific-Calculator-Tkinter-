import tkinter as tk
from math import sin, cos, tan, log, sqrt, pi, e, radians

class SciCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.equation = ""
        self.mode = "DEG"
        self.input_text = tk.StringVar()

        self.create_display()
        self.create_buttons()
        self.create_mode_toggle()

    def create_display(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="both")

        input_field = tk.Entry(input_frame, textvariable=self.input_text,
                               font=('arial', 20), bd=5, relief="ridge", justify="right")
        input_field.pack(fill="both", ipadx=8, ipady=20)

    def create_mode_toggle(self):
        toggle_frame = tk.Frame(self.root)
        toggle_frame.pack(fill="x", pady=(0, 5))
        
        self.mode_label = tk.Label(toggle_frame, text=f"Mode: {self.mode}", font=('arial', 12))
        self.mode_label.pack(side="left", padx=10)

        toggle_btn = tk.Button(toggle_frame, text="Toggle DEG/RAD", font=('arial', 12),
                               command=self.toggle_mode)
        toggle_btn.pack(side="right", padx=10)

    def toggle_mode(self):
        self.mode = "RAD" if self.mode == "DEG" else "DEG"
        self.mode_label.config(text=f"Mode: {self.mode}")

    def create_buttons(self):
        btns_frame = tk.Frame(self.root)
        btns_frame.pack(expand=True, fill="both")

        buttons = [
            ['7', '8', '9', '/', 'sin'],
            ['4', '5', '6', '*', 'cos'],
            ['1', '2', '3', '-', 'tan'],
            ['0', '.', 'sqrt', '+', 'log'],
            ['(', ')', 'pi', 'e', 'C'],
            ['=', '', '', '', '']
        ]

        for i in range(len(buttons)):
            btns_frame.rowconfigure(i, weight=1)
            for j in range(len(buttons[i])):
                btns_frame.columnconfigure(j, weight=1)
                btn_text = buttons[i][j]
                if btn_text:
                    btn = tk.Button(btns_frame, text=btn_text, font=('arial', 14),
                                    command=lambda x=btn_text: self.click_event(x))
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

    def click_event(self, key):
        if key == "=":
            try:
                result = str(self.safe_eval(self.equation))
                self.input_text.set(result)
                self.equation = result
            except Exception:
                self.input_text.set("Error")
                self.equation = ""
        elif key == "C":
            self.equation = ""
            self.input_text.set("")
        else:
            self.equation += str(key)
            self.input_text.set(self.equation)

    def safe_eval(self, expr):
        # Define functions for DEG/RAD
        def sin_custom(x): return sin(radians(x)) if self.mode == "DEG" else sin(x)
        def cos_custom(x): return cos(radians(x)) if self.mode == "DEG" else cos(x)
        def tan_custom(x): return tan(radians(x)) if self.mode == "DEG" else tan(x)

        # Eval-safe dictionary
        allowed_names = {
            'sin': sin_custom,
            'cos': cos_custom,
            'tan': tan_custom,
            'sqrt': sqrt,
            'log': log,
            'pi': pi,
            'e': e,
            '__builtins__': {}
        }

        return eval(expr, allowed_names)

# Run the calculator
if __name__ == "__main__":
    root = tk.Tk()
    app = SciCalc(root)
    root.mainloop()
