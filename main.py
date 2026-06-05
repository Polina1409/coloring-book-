import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# 1. Создаем контур (белый лист с черными фигурами)
img = Image.new('RGB', (600, 400), 'white')
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 250, 350], outline='black', width=5)
draw.ellipse([350, 50, 550, 350], outline='black', width=5)

color = "#FF0000" # Текущий цвет (красный по умолчанию)

def paint(event):
    """Заливка области при клике"""
    rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    ImageDraw.floodfill(img, (event.x, event.y), value=rgb)
    update()

def set_color(new_color):
    global color
    color = new_color

def update():
    """Обновление картинки на экране"""
    global tk_img
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor="nw", image=tk_img)

# 2. Настройка окна
root = tk.Tk()
root.title("Мини-Раскраска")

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()
canvas.bind("<Button-1>", paint)

# 3. Кнопки управления
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Красный", bg="red", command=lambda: set_color("#FF0000")).pack(side="left")
tk.Button(btn_frame, text="Зеленый", bg="green", command=lambda: set_color("#00FF00")).pack(side="left")
tk.Button(btn_frame, text="Синий", bg="blue", fg="white", command=lambda: set_color("#0000FF")).pack(side="left")

update()
root.mainloop()