import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
class ColoringGameStep3:
    def __init__(self, root):
        self.root = root
        self.root.title("Winx: Волшебницы цвета")
        self.current_color = "pink"
        self.buttons = {}
        self.image_files = {
            "Блум (Цветок)": "bloom.png",
            "Стелла (Звезда)": "stella.png",
            "Флора (Кристалл)": "flora.png"
        }
        self.current_key = "Блум (Цветок)"
        self.base_images = {}
        self.load_all_contours()
        self.current_img = self.base_images[self.current_key].copy()
        left_panel = tk.Frame(root, bg='#FFE4E1')
        left_panel.pack(side='left', fill='y', padx=10, pady=10)
        tk.Label(left_panel, text="Рисунки", font=("Arial", 12, "bold"), bg='#FFE4E1').pack(pady=5)
        for name in self.image_files.keys():
            tk.Button(left_panel, text=name, font=("Arial", 10), width=15,
                      command=lambda n=name: self.switch_image(n)).pack(pady=4, padx=10)
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white', cursor="pencil")
        self.canvas.pack(side='left', padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.fill_area)
        right_panel = tk.Frame(root)
        right_panel.pack(side='right', fill='y', padx=20, pady=20)
        tk.Label(right_panel, text="Палитра", font=("Arial", 12, "bold")).pack(pady=5)
        colors = ["#FF1493", "#FF3307", "#FF6B00", "#FFD700", "#228B22", "#00BFFF", "#8A2BE2", "#FFFFFF"]
        for c in colors:
            btn = tk.Button(right_panel, bg=c, width=8, height=1, command=lambda col=c: self.set_color(col))
            btn.pack(pady=3)
            self.buttons[c] = btn
        tk.Button(right_panel, text="Сохранить ✨", bg="#98FB98", font=("Arial", 10, "bold"),
                  command=self.save_image).pack(side='bottom', pady=10, fill='x')
        tk.Button(right_panel, text="Очистить", bg="#FFB6C1", font=("Arial", 10, "bold"),
                  command=self.clear_canvas).pack(side='bottom', pady=10, fill='x')
        self.set_color(self.current_color)
        self.render_image()
    def load_all_contours(self):
        for name, filename in self.image_files.items():
            if os.path.exists(filename):
                try:
                    img = Image.open(filename).convert('RGB')
                    img = img.resize((600, 600), Image.Resampling.LANCZOS)
                    self.base_images[name] = img
                    continue
                except Exception as e:
                    print(f"Ошибка чтения {filename}: {e}")
            self.base_images[name] = self.generate_fallback_shape(name)
    def generate_fallback_shape(self, name):
        img = Image.new('RGB', (600, 600), 'white')
        draw = ImageDraw.Draw(img)
        if "Блум" in name:
            for x, y in [(150, 100), (350, 100), (150, 300), (350, 300)]:
                draw.ellipse([x, y, x + 100, y + 100], outline='black', width=3)
            draw.ellipse([225, 175, 375, 325], fill='white', outline='black', width=4)
        elif "Стелла" in name:
            draw.polygon([(300, 50), (350, 200), (500, 200), (380, 300), (430, 450), (300, 350), (170, 450), (220, 300),
                          (100, 200), (250, 200)], outline='black', width=4)
        else:
            draw.polygon([(300, 50), (500, 300), (300, 550), (100, 300)], outline='black', width=4)
            draw.line([(300, 50), (300, 550)], fill='black', width=2)
            draw.line([(100, 300), (500, 300)], fill='black', width=2)
        return img
    def switch_image(self, name):
        self.current_key = name
        self.clear_canvas()
    def set_color(self, selected_color):
        self.current_color = selected_color
        for btn in self.buttons.values():
            btn.config(relief='raised', bd=2)
        if selected_color in self.buttons:
            self.buttons[selected_color].config(relief='sunken', bd=4)
    def render_image(self):
        self.tk_img = ImageTk.PhotoImage(self.current_img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
    def fill_area(self, event):
        x, y = event.x, event.y
        if 0 <= x < self.current_img.width and 0 <= y < self.current_img.height:
            rgb = self.root.winfo_rgb(self.current_color)
            rgb_tuple = (rgb[0] // 256, rgb[1] // 256, rgb[2] // 256)
            ImageDraw.floodfill(self.current_img, (x, y), rgb_tuple)
            self.render_image()
    def clear_canvas(self):
        self.current_img = self.base_images[self.current_key].copy()
        self.render_image()
    def save_image(self):
        default_name = f"my_{self.current_key.lower().split()[0]}.png"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            initialfile=default_name,
            title="Сохранить раскраску"
        )
        if file_path:
            self.current_img.save(file_path, "PNG")
            print(f"Рисунок успешно сохранен: {file_path}")
if __name__ == "__main__":
    root = tk.Tk()
    app = ColoringGameStep3(root)
    root.mainloop()