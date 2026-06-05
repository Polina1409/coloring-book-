import tkinter as tk
import os
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageOps
class WinxColoringGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Winx: Волшебницы цвета")
        # Ограничение по минимальному размеру
        self.root.minsize(1024, 768)
        # Размер окна при запуске
        self.root.geometry("1200x800")
        # Развернуть на весь экран
        try:
            self.root.state('zoomed')
        except:
            pass
        self.start_img_path = "start_logo.png"
        #Палитра
        self.colors_dict = {
            "темнокр": "#8B0000", "красный": "#FF3307", "малиновый": "#D12D69",
            "Неоново-розовый": "#FF1493", "фуксия": "#FF00FF", "лиловый": "#EF84B0",
            "оранжевый": "#FF6B00", "светлоор": "#FFA75D", "золотой": "#FFD700",
            "лимонный": "#FFF96D", "лесной": "#228B22", "изумрудный": "#00C957",
            "свзеленый": "#98FB98", "светло-зеленый": "#DEF5A3", "мятный": "#7FFFD4",
            "Бирюзовый": "#00FFFF", "Аквамариновый": "#00CED1", "Морская волна": "#2F4F4F",
            "оливковый": "#808000", "Небесный": "#87CEEB", "голубой": "#67CBED",
            "Электрический голубой": "#00BFFF", "синий": "#0072A4", "Тёмно-синий": "#00008B",
            "темно-синий": "#190A45", "Холодный фиолетовый": "#8A2BE2", "светло-фиолетовый": "#A64CE3",
            "аметист": "#9966CC", "фиолетовый": "#6D5D9C", "сиреневый": "#C8A2C8",
            "лавандовый": "#E6E6FA", "коричневый": "#BE7F18", "болотный": "#734A12",
            "бежевый": "#FCD1A6", "белый": "#FFFFFF", "Серебряный": "#C0C0C0",
            "Стальной серый": "#708090", "черный": "#000000"
        }
        self.colors = list(self.colors_dict.values())
        # Стартовый цвет
        self.current_color = self.colors[0]
        self.images = {}
        self.current_image_key = None
        self.current_pil_image = None
        self.tk_image = None
        self.start_tk_image = None
        # Подготовка картинок
        self.load_all_contours()
        # Запуск стартового экрана
        self.create_start_screen()
    def load_all_contours(self):
        #загрузка картинок из файла
        img_keys = {
            "Блум": "blum.png",
            "Флора": "flora.png",
            "Лейла": "leyla.png",
            "Муза": "muza.png",
            "Стелла": "stella.png",
            "Текна": "tecna.png",
            "Общее фото": "all.png"
        }
         #размеры холста
        max_w, max_h = 900, 700
        for key, file_name in img_keys.items():
            if os.path.exists(file_name):
                try:
                    img_gray = Image.open(file_name).convert('L')
                    # убираем серые пиксели, делая контур четким
                    img_bin = img_gray.point(lambda p: 0 if p < 220 else 255)
                    img_rgb = img_bin.convert('RGB')
                    # Сжимаем/расширяем картинку с сохранением пропорций
                    img_resized = ImageOps.contain(img_rgb, (max_w, max_h), Image.Resampling.LANCZOS)
                    final_img = Image.new('RGB', img_resized.size, 'white')
                    final_img.paste(img_resized, (0, 0))
                    self.images[key] = final_img
                except Exception as e:
                    print(f"Ошибка при обработке {file_name}: {e}")
                    self.create_fallback_image(key)
            else:
                self.create_fallback_image(key)
    def create_fallback_image(self, key):
        #создание простых фигур при отсутствии картинки в папке
        img = Image.new('RGB', (900, 700), 'white')
        draw = ImageDraw.Draw(img)
        draw.rectangle([150, 150, 350, 550], outline='black', width=3)
        draw.ellipse([450, 150, 650, 350], outline='black', width=3)
        draw.polygon([(450, 450), (550, 550), (650, 450)], outline='black', width=3)
        draw.text((30, 30), f"Контур: {key}\n(Добавьте файл {key.lower()}.png в папку)", fill="black")
        self.images[key] = img
    def clear_window(self):
        #очистка окна при переключении
        for widget in self.root.winfo_children():
            widget.destroy()
    def create_start_screen(self):
        #гланое меню
        self.clear_window()
        start_frame = tk.Frame(self.root, bg='white')
        start_frame.pack(expand=True, fill='both')
        img_label = None
        if os.path.exists(self.start_img_path):
            try:
                pil_start_img = Image.open(self.start_img_path)
                pil_start_img = pil_start_img.resize((500, 350), Image.Resampling.LANCZOS)
                self.start_tk_image = ImageTk.PhotoImage(pil_start_img)
                img_label = tk.Label(start_frame, image=self.start_tk_image, bg='white')
            except Exception as e:
                print(f"Ошибка загрузки логотипа: {e}")
        if img_label is None:
            img_label = tk.Label(
                start_frame,
                text=f"Логотип Winx\n(Поместите файл '{self.start_img_path}' в папку)",
                bg="#FFC0CB", fg="#D11A5B", font=("Arial", 14, "italic"), width=65, height=8, relief="groove", bd=2
            )
        img_label.pack(pady=(60, 20))
        title = tk.Label(start_frame, text="Winx: Волшебницы цвета", font=("Arial", 36, "bold"), bg='white')
        title.pack(pady=20)
        # кнопка "старт"
        start_canvas = tk.Canvas(start_frame, width=120, height=120, bg='white', highlightthickness=0, cursor="hand2")
        start_canvas.pack(pady=20, anchor="e", padx=120)
        start_canvas.create_oval(5, 5, 115, 115, fill="#FF69B4", outline="#D11A5B", width=3)
        start_canvas.create_text(60, 60, text="СТАРТ", font=("Arial", 20, "bold"), fill="white")
        start_canvas.bind("<Button-1>", lambda event: self.create_game_screen())

    def create_game_screen(self):
        # игровое поле
        self.clear_window()
        game_frame = tk.Frame(self.root)
        game_frame.pack(expand=True, fill='both')

        # Верхняя панель
        top_panel = tk.Frame(game_frame, height=60, bg='#FFE4E1', bd=2, relief='groove')
        top_panel.pack(side='top', fill='x')

        tk.Label(top_panel, text="Winx", font=("Arial", 18, "bold"), bg='#FFE4E1', fg='#FF1493').pack(side='left',
                                                                                                      padx=30, pady=15)

        tk.Button(top_panel, text="Очистить", font=("Arial", 12, "bold"), width=12, command=self.clear_image).pack(
            side='left', padx=15)
        tk.Button(top_panel, text="Сохранить", font=("Arial", 12, "bold"), width=12, command=self.save_image).pack(
            side='left', padx=15)
        tk.Button(top_panel, text="Закрыть", font=("Arial", 12), bg='#FFB6C1', command=self.root.destroy).pack(
            side='right', padx=30)

        # Левая панель
        left_panel = tk.Frame(game_frame, width=180, bg='#E6E6FA', bd=2, relief='groove')
        left_panel.pack(side='left', fill='y')
        tk.Label(left_panel, text="Выбор рисунка", font=("Arial", 12, "bold"), bg='#E6E6FA').pack(pady=15)
        for key in self.images.keys():
            tk.Button(left_panel, text=key, font=("Arial", 11), width=14, height=2,
                      command=lambda k=key: self.load_image(k)).pack(pady=6, padx=15)

        # Правая панель
        right_panel = tk.Frame(game_frame, width=160, bg='#E6E6FA', bd=2, relief='groove')
        right_panel.pack(side='right', fill='y')
        tk.Label(right_panel, text="Палитра", font=("Arial", 12, "bold"), bg='#E6E6FA').pack(pady=10)

        # текущий цвет
        self.color_indicator = tk.Label(right_panel, text="Текущий", font=("Arial", 10, "bold"), bg=self.current_color,
                                        width=12, height=2)
        self.color_indicator.pack(pady=5, padx=10)

        buttons_frame = tk.Frame(right_panel, bg='#E6E6FA')
        buttons_frame.pack(pady=5)

        # сетка цветов
        for index, color in enumerate(self.colors):
            row = index // 2
            col = index % 2
            btn = tk.Button(buttons_frame, bg=color, width=4, height=1, activebackground=color,
                            command=lambda c=color: self.set_color(c))
            btn.grid(row=row, column=col, padx=3, pady=1)

        # Центральная зона
        self.canvas_frame = tk.Frame(game_frame, bg='white')
        self.canvas_frame.pack(side='left', expand=True, fill='both')
        self.canvas = tk.Canvas(self.canvas_frame, bg='white', cursor="target")
        self.canvas.pack(expand=True, fill='both')
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.load_image("Общее фото")
    def load_image(self, key):
        #Загрузка выбранной картинки на экран
        self.current_image_key = key
        self.current_pil_image = self.images[key].copy()
        self.update_canvas()
    def update_canvas(self):
        # обновление холста
        if self.current_pil_image:
            self.tk_image = ImageTk.PhotoImage(self.current_pil_image)
            self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)
    def set_color(self, color):
        #Смена активного цвета
        self.current_color = color
        self.color_indicator.config(bg=color)
    def on_canvas_click(self, event):
        #алгоритм заливки
        if not self.current_pil_image:
            return
        img_x, img_y = event.x, event.y
        # Проверка клика внутри картинки
        if 0 <= img_x < self.current_pil_image.width and 0 <= img_y < self.current_pil_image.height:
            try:
                rgb_color = self.hex_to_rgb(self.current_color)
                ImageDraw.floodfill(self.current_pil_image, (img_x, img_y), value=rgb_color, thresh=50)
                self.update_canvas()
            except Exception as e:
                print(f"Ошибка при заливке: {e}")
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    def clear_image(self):
        #Кнопка 'Очистить'
        if self.current_image_key:
            self.load_image(self.current_image_key)
    def save_image(self):
        #Кнопка 'Сохранить'
        if self.current_pil_image:
            filename = datetime.now().strftime("winx_save_%Y%m%d_%H%M%S.png")
            self.current_pil_image.save(filename, "PNG")
            print(f"Успешно сохранено на устройство: {filename}")
if __name__ == "__main__":
    root = tk.Tk()
    app = WinxColoringGame(root)
    root.mainloop()

