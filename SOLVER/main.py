import tkinter as tk
from tkinter import messagebox
import kociemba

class DynamicRubiksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik Solver - Generátor Stringu")
        self.root.resizable(False, False)
        
        # Paleta 6 barev
        self.colors = ["white", "red", "green", "yellow", "orange", "blue"]
        
        # Inicializace stavu: 6 stran, každá má 9 políček
        self.cube_state = [[self.colors[i]] * 9 for i in range(6)]
        
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#2c3e50")
        main_frame.pack()

        tk.Label(main_frame, text="Nastavte barvy (Střed definuje stranu)", 
                 fg="white", bg="#2c3e50", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=5, pady=10)

        # Rozvržení stran: 0:Up, 1:Right, 2:Front, 3:Down, 4:Left, 5:Back
        layout = {
            0: (1, 2), 4: (2, 1), 2: (2, 2), 
            1: (2, 3), 5: (2, 4), 3: (3, 2)
        }

        self.buttons = []
        for side in range(6):
            side_frame = tk.Frame(main_frame, bd=2, relief="flat", bg="#34495e")
            r, c = layout[side]
            side_frame.grid(row=r, column=c, padx=5, pady=5)
            
            side_buttons = []
            for i in range(9):
                btn = tk.Button(side_frame, width=3, height=1, 
                                bg=self.cube_state[side][i],
                                command=lambda s=side, p=i: self.rotate_color(s, p))
                btn.grid(row=i//3, column=i%3, padx=1, pady=1)
                side_buttons.append(btn)
            self.buttons.append(side_buttons)

        # --- NOVÉ: POLE PRO KOCIEMBA STRING ---
        tk.Label(main_frame, text="Kociemba String (pro kopírování):", fg="#ecf0f1", bg="#2c3e50").grid(row=4, column=0, columnspan=5, pady=(10, 0))
        self.string_var = tk.StringVar()
        self.string_entry = tk.Entry(main_frame, textvariable=self.string_var, width=60, font=("Courier", 10))
        self.string_entry.grid(row=5, column=0, columnspan=5, pady=5)

        # Tlačítka
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.grid(row=6, column=0, columnspan=5, pady=15)

        tk.Button(btn_frame, text="VYŘEŠIT A GENEROVAT", font=("Arial", 10, "bold"),
                  bg="#e67e22", fg="white", padx=20, command=self.solve_cube).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="RESET", font=("Arial", 10),
                  bg="#95a5a6", fg="white", command=self.reset_cube).pack(side=tk.LEFT, padx=5)

        self.result_text = tk.Text(main_frame, height=3, width=50, font=("Courier", 11), 
                                  bg="#ecf0f1", state="disabled")
        self.result_text.grid(row=7, column=0, columnspan=5, pady=10)

    def rotate_color(self, side, pos):
        current_color = self.cube_state[side][pos]
        next_idx = (self.colors.index(current_color) + 1) % len(self.colors)
        new_color = self.colors[next_idx]
        
        self.cube_state[side][pos] = new_color
        self.buttons[side][pos].config(bg=new_color)

    def get_dynamic_mapping(self):
        mapping = {}
        order = ["U", "R", "F", "D", "L", "B"]
        
        for side in range(6):
            center_color = self.cube_state[side][4]
            if center_color in mapping:
                return None
            mapping[center_color] = order[side]
            
        return mapping

    def solve_cube(self):
        color_to_letter = self.get_dynamic_mapping()
        
        if not color_to_letter:
            messagebox.showerror("Chyba", "Každý střed musí mít unikátní barvu!")
            return

        # Sestavení řetězce
        k_string = ""
        try:
            for side in range(6):
                for pos in range(9):
                    color = self.cube_state[side][pos]
                    k_string += color_to_letter[color]
            
            # Zobrazení stringu v poli pro kopírování
            self.string_var.set(k_string)
            
            # Výpočet řešení
            solution = kociemba.solve(k_string)
            self.display_result(solution)
        except Exception as e:
            messagebox.showerror("Chyba", f"Kostku nelze vyřešit: {e}")

    def reset_cube(self):
        for side in range(6):
            for pos in range(9):
                self.cube_state[side][pos] = self.colors[side]
                self.buttons[side][pos].config(bg=self.colors[side])
        self.string_var.set("")
        self.display_result("")

    def display_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        if text:
            self.result_text.insert(tk.END, f"Tah k vyřešení:\n{text}")
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicRubiksApp(root)
    root.mainloop()