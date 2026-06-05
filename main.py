import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw
class ColoringGameStep1:
    def __init__(self, root):
        self.root = root
        self.root.title("Winx: Магия Цвета (Шаг 1)")
        self.current_color = "pink"
        self.buttons = {}
        self.image_filename = "winx_contour.png"
        self.base_img = self.load_contour()
        self.current_img = self.base_img.copy()
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white', cursor="pencil")
        self.canvas.pack(side='left', padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.fill_area)
        panel = tk.Frame(root)
        panel.pack(side='right', fill='y', padx=20, pady=20)
        tk.Label(panel, text="Палитра", font=("Arial", 12, "bold")).pack(pady=5)
        colors = ["#FF1493", "#FF3307", "#FF6B00", "#FFD700", "#228B22", "#00BFFF", "#8A2BE2", "#FFFFFF"]
        for c in colors:
            btn = tk.Button(panel, bg=c, width=8, height=1, command=lambda col=c: self.set_color(col))
            btn.pack(pady=3)
            self.buttons[c] = btn
        tk.Button(panel, text="Очистить", bg="#FFB6C1", font=("Arial", 10, "bold"),
                  command=self.clear_canvas).pack(side='bottom', pady=20, fill='x')
        self.set_color(self.current_color)
        self.render_image()
    def load_contour(self):
        if os.path.exists(self.image_filename):
            try:
                img = Image.open(self.image_filename).convert('RGB')
                img = img.resize((600, 600), Image.Resampling.LANCZOS)
                return img
            except Exception as e:
                print(f"Не удалось прочитать файл. Ошибка: {e}")
        img = Image.new('RGB', (600, 600), 'white')
        draw = ImageDraw.Draw(img)
        for x, y in [(150, 100), (350, 100), (150, 300), (350, 300)]:
            draw.ellipse([x, y, x + 100, y + 100], outline='black', width=3)
        draw.ellipse([225, 175, 375, 325], fill='white', outline='black', width=4)
        return img
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
        self.current_img = self.base_img.copy()
        self.render_image()
if __name__ == "__main__":
    root = tk.Tk()
    app = ColoringGameStep1(root)
    root.mainloop()