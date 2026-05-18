#A small section so that anyone who worked on the code/version has a mention of them

#Original concept and code by: HeliX475
#Version by: <your nickname/nicknames>

import tkinter as tk
from tkinter import ttk

class ShrempleDecoder:
    def __init__(self, root, hex_data):
        self.root = root
        self.root.title("Shremple Sliding Window Decoder")
        
        self.bit_str = "".join([bin(int(h, 16))[2:].zfill(32) for h in hex_data])
        
        #Hardcoded end temple coordinates (val) and window size (which I calculated manually based on the required number of bits per coordinate)
        #If you want to change the coordinates you're looking for, change the val.
        #Remember to also change the size to match the number of bits needed for that number. I didn't do a value->bit size conversion, sorry.
        #To check how large size must be, check if 2^n gives a number larger than the searched number, but not too much either.
        #For example,when searching for X 1607000, we need 21 bits because: 2^21 allows us to store 2097152 while 2^20 is too small
        #because it can only store up to 1048576.
        
        self.targets = {
            "X": {"val": 1607000, "size": 21, "rgb": (255, 0, 0), "label": "X (Red)"},
            "Y": {"val": 3500000, "size": 22, "rgb": (0, 255, 0), "label": "Y (Green)"},
            "Z": {"val": 439000, "size": 19, "rgb": (0, 0, 255), "label": "Z (Blue)"}
        }
        
        self.layers = {i: [False, False, False] for i in range(512)}
        self.setup_ui()
        self.draw_matrix()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0)

        self.canvas = tk.Canvas(main_frame, width=480, height=360, bg="#111")
        self.canvas.grid(row=0, column=0, padx=10)

        self.legenda = tk.Frame(main_frame, bg="#111", pady=10)
        self.legenda.grid(row=1, column=0, columnspan=2, sticky="we")
        
        def add_leg(txt, clr):
            tk.Label(self.legenda, text=txt, fg=clr, bg="#111", font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=10)

        add_leg("X", "#ff4444"); add_leg("Y", "#44ff44"); add_leg("Z", "#4444ff")
        add_leg("X+Y", "yellow"); add_leg("Y+Z", "cyan"); add_leg("X+Z", "magenta")

        self.results_text = tk.Text(main_frame, width=65, height=22, bg="#1e1e1e", fg="#eee", font=("Consolas", 9))
        self.results_text.grid(row=0, column=1, padx=10)
        
        btn_scan = ttk.Button(main_frame, text="ANALYZE WINDOWS", command=self.scan_and_mix)
        btn_scan.grid(row=1, column=1, sticky="e", pady=10)

    def get_mixed_color(self, idx):
        is_one = self.bit_str[idx] == '1'
        r, g, b = self.layers[idx]
        
        if not any([r, g, b]):
            return "#ffffff" if is_one else "#222"
            
        # Brightness selection: 255 for 1 and 60 for 0 (to have a darker shade)
        intensity = 255 if is_one else 60
        
        res_r = intensity if r else 0
        res_g = intensity if g else 0
        res_b = intensity if b else 0
        
        return '#%02x%02x%02x' % (res_r, res_g, res_b)

    def draw_matrix(self):
        self.canvas.delete("all")
        cell_w, cell_h = 12, 18
        offset_x = 45 
        
        for line_num in range(16):
            y_pos = line_num * cell_h + 15
            self.canvas.create_text(20, y_pos + 10, text=f"{line_num + 1})", fill="#666", font=("Consolas", 10))
            
            for bit_pos in range(32):
                idx = line_num * 32 + bit_pos
                color = self.get_mixed_color(idx)
                
                x_start = bit_pos * cell_w + offset_x
                border = "#444" if any(self.layers[idx]) else "#222"
                self.canvas.create_rectangle(
                    x_start, y_pos, x_start + cell_w, y_pos + cell_h, 
                    fill=color, outline=border
                )

    def scan_and_mix(self):
        self.results_text.delete(1.0, tk.END)
        self.layers = {i: [False, False, False] for i in range(512)}
        ext_bits = self.bit_str + self.bit_str[:64]
        
        header = f"{'TYPE':<4} | {'LINE':<6} | {'BIT':<3} | {'VALUE':<10} | {'DIFF'}\n"
        self.results_text.insert(tk.END, header + "="*65 + "\n")

        for key, data in self.targets.items():
            best_diff = float('inf')
            best_pos, best_val, best_bin = 0, 0, ""
            
            for i in range(512):
                chunk = ext_bits[i : i + data["size"]]
                val = int(chunk, 2)
                diff = abs(val - data["val"])
                if diff < best_diff:
                    best_diff, best_pos, best_val, best_bin = diff, i, val, chunk
            
            l_idx = 0 if key == "X" else 1 if key == "Y" else 2
            for offset in range(data["size"]):
                self.layers[(best_pos + offset) % 512][l_idx] = True

            ln, bt = (best_pos // 32) + 1, (best_pos % 32) + 1
            self.results_text.insert(tk.END, f"{key:<4} | L:{ln:<4} | B:{bt:<2} | {best_val:<10} | {best_diff}\n")
            self.results_text.insert(tk.END, f" BIN: [{best_bin}]\n{'-'*65}\n")

        self.draw_matrix()

#Hex data from all towers
HEX_DATA = ["5755555D", "80081010", "09808001", "80008109", "00020400", "704A028E", "02000000", "92202020", "0892A000", "80029024", "42402111", "32000451", "0200C040", "9C1C1D1F", "3D5C1C9C", "1C1C1C1C"]

if __name__ == "__main__":
    root = tk.Tk()
    app = ShrempleDecoder(root, HEX_DATA)
    root.mainloop()
