import math
import tkinter as tk
from tkinter import font

W, H = 380, 600

# Palette
BG = "#FFB6C1"
FRAME = "#FFD1DC"
SCREEN = "#FFF0F5"
INK = "#4A0E17"
NUM_BG = "#FFE4E1"
TOP_BG = "#FADADD"
OP_BG = "#FF69B4"
PRESS_BG = "#FFB6C1"
SHADOW = "#E8A0B8"
CREAM = "#FFFDD0"
DARK_PINK = "#C71585"
PETAL = "#E0529C"
PETAL_LIGHT = "#FF9CC8"
GOLD = "#E0A21F"


class PinkCalculator(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Soft Pink Calculator")
        self.geometry(f"{W}x{H}")
        self.resizable(False, False)

        # State
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.reset_screen = False
        self.error = False

        self.canvas = tk.Canvas(self, width=W, height=H, highlightthickness=0, bg=BG)
        self.canvas.pack(fill="both", expand=True)

        self.draw_background_pattern()
        self.build_ui()
        self.bind("<Key>", self.key_press)

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def rounded_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.canvas.create_polygon(pts, smooth=True, **kw)

    @staticmethod
    def ellipse_points(cx, cy, rx, ry, rot, n=18):
        pts = []
        cr, sr = math.cos(rot), math.sin(rot)
        for i in range(n):
            t = 2 * math.pi * i / n
            ex, ey = rx * math.cos(t), ry * math.sin(t)
            pts += [cx + ex * cr - ey * sr, cy + ex * sr + ey * cr]
        return pts

    def draw_flower(self, x, y, scale=1.0, spin=0.0):
        c = self.canvas
        # Outer petals
        for k in range(6):
            a = math.radians(60 * k) + spin
            px = x + math.sin(a) * 7.5 * scale
            py = y - math.cos(a) * 7.5 * scale
            c.create_polygon(
                self.ellipse_points(px, py, 4.2 * scale, 7.5 * scale, a),
                smooth=True, fill=PETAL, outline=DARK_PINK, width=1,
            )
        # Inner petals (lighter)
        for k in range(6):
            a = math.radians(60 * k) + spin
            px = x + math.sin(a) * 6.0 * scale
            py = y - math.cos(a) * 6.0 * scale
            c.create_polygon(
                self.ellipse_points(px, py, 2.2 * scale, 4.6 * scale, a),
                smooth=True, fill=PETAL_LIGHT, outline="",
            )
        # Center
        r = 3.6 * scale
        c.create_oval(x - r, y - r, x + r, y + r, fill=CREAM, outline="")
        # Golden dots
        for k in range(5):
            a = 2 * math.pi * k / 5
            dx, dy = x + math.cos(a) * 1.9 * scale, y + math.sin(a) * 1.9 * scale
            d = 0.8 * scale
            c.create_oval(dx - d, dy - d, dx + d, dy + d, fill=GOLD, outline="")

    def draw_heart(self, x, y, s=0.45):
        pts = []
        for i in range(36):
            t = 2 * math.pi * i / 36
            hx = 16 * math.sin(t) ** 3
            hy = -(13 * math.cos(t) - 5 * math.cos(2 * t)
                   - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts += [x + hx * s, y + hy * s]
        self.canvas.create_polygon(pts, fill=DARK_PINK, outline=DARK_PINK)

    def draw_sparkle(self, x, y, s=1.3):
        base = [0, -3, .8, -.8, 3, 0, .8, .8, 0, 3, -.8, .8, -3, 0, -.8, -.8]
        pts = []
        for i in range(0, len(base), 2):
            pts += [x + base[i] * s, y + base[i + 1] * s]
        self.canvas.create_polygon(pts, fill=CREAM, outline="")

    def draw_background_pattern(self):
        self.canvas.create_rectangle(0, 0, W, H, fill=BG, outline=BG)
        for ty in range(-45, H + 45, 90):
            for tx in range(-45, W + 45, 90):
                self.draw_flower(tx + 67, ty + 22, 1.0)
                self.draw_flower(tx + 22, ty + 67, 0.85, math.radians(18))
                self.draw_heart(tx + 22, ty + 22)
                self.draw_heart(tx + 67, ty + 67)
                self.draw_sparkle(tx + 45, ty + 45)
                self.draw_sparkle(tx, ty, 1.0)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def build_ui(self):
        c = self.canvas

        # Soft frame with shadow
        fx1, fy1, fx2, fy2 = 30, 60, 350, 477
        self.rounded_rect(fx1, fy1 + 6, fx2, fy2 + 6, 32, fill=SHADOW, outline="")
        self.rounded_rect(fx1, fy1, fx2, fy2, 32, fill=FRAME, outline="")

        # Display (sunken look)
        dx1, dy1, dx2, dy2 = fx1 + 18, fy1 + 18, fx2 - 18, fy1 + 84
        self.rounded_rect(dx1, dy1, dx2, dy2, 24, fill="#F5C6D6", outline="")
        self.rounded_rect(dx1, dy1 + 3, dx2, dy2, 24, fill=SCREEN, outline="")
        self.display_font = font.Font(family="Helvetica", size=26, weight="bold")
        self.display_id = c.create_text(
            dx2 - 20, (dy1 + dy2) / 2 + 2, text="0", anchor="e",
            font=self.display_font, fill=INK,
        )

        # Buttons: (label, value, row, col, colspan, kind)
        buttons = [
            ("AC", "AC", 0, 0, 2, "top"),
            ("±", "±", 0, 2, 1, "top"),
            ("÷", "/", 0, 3, 1, "op"),
            ("7", "7", 1, 0, 1, "num"),
            ("8", "8", 1, 1, 1, "num"),
            ("9", "9", 1, 2, 1, "num"),
            ("×", "*", 1, 3, 1, "op"),
            ("4", "4", 2, 0, 1, "num"),
            ("5", "5", 2, 1, 1, "num"),
            ("6", "6", 2, 2, 1, "num"),
            ("−", "-", 2, 3, 1, "op"),
            ("1", "1", 3, 0, 1, "num"),
            ("2", "2", 3, 1, 1, "num"),
            ("3", "3", 3, 2, 1, "num"),
            ("+", "+", 3, 3, 1, "op"),
            ("0", "0", 4, 0, 2, "num"),
            (".", ".", 4, 2, 1, "num"),
            ("=", "=", 4, 3, 1, "op"),
        ]

        gap = 10
        top = dy2 + 15
        bw = (fx2 - fx1 - 36 - 3 * gap) / 4
        bh = 52
        btn_font = font.Font(family="Helvetica", size=14, weight="bold")

        for i, (label, value, row, col, span, kind) in enumerate(buttons):
            x1 = fx1 + 18 + col * (bw + gap)
            x2 = x1 + span * bw + (span - 1) * gap
            y1 = top + row * (bh + gap)
            y2 = y1 + bh

            if kind == "op":
                bg, fg = OP_BG, "#FFFFFF"
            elif kind == "top":
                bg, fg = TOP_BG, INK
            else:
                bg, fg = NUM_BG, INK

            tag = f"btn{i}"
            self.rounded_rect(x1, y1 + 3, x2, y2 + 3, bh / 2, fill=SHADOW,
                              outline="", tags=(tag,))
            pill = self.rounded_rect(x1, y1, x2, y2, bh / 2, fill=bg,
                                     outline="", tags=(tag,))
            text = c.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=label,
                                 font=btn_font, fill=fg, tags=(tag,))
            self.bind_button(tag, pill, text, bg, fg, value)

        # Footer
        c.create_text(
            W / 2, 565, text="Built by Amna Sahar",
            fill=CREAM, font=("Helvetica", 10, "italic"),
        )

    def bind_button(self, tag, pill, text, bg, fg, value):
        c = self.canvas
        state = {"down": False}

        def press(_e):
            state["down"] = True
            c.itemconfig(pill, fill=PRESS_BG)
            c.itemconfig(text, fill="#FFFFFF")
            c.move(pill, 0, 2)
            c.move(text, 0, 2)

        def release_visual():
            if state["down"]:
                state["down"] = False
                c.itemconfig(pill, fill=bg)
                c.itemconfig(text, fill=fg)
                c.move(pill, 0, -2)
                c.move(text, 0, -2)

        def release(_e):
            was_down = state["down"]
            release_visual()
            if was_down:
                self.on_button_click(value)

        c.tag_bind(tag, "<ButtonPress-1>", press)
        c.tag_bind(tag, "<ButtonRelease-1>", release)
        c.tag_bind(tag, "<Leave>", lambda _e: (release_visual(), c.config(cursor="")))
        c.tag_bind(tag, "<Enter>", lambda _e: c.config(cursor="hand2"))

    # ------------------------------------------------------------------
    # Calculator logic
    # ------------------------------------------------------------------
    def on_button_click(self, char):
        if self.error:
            self.clear_all()
        if char.isdigit():
            self.handle_number(char)
        elif char == ".":
            self.handle_decimal()
        elif char in ("+", "-", "*", "/"):
            self.handle_operator(char)
        elif char == "=":
            self.calculate_result()
        elif char == "AC":
            self.clear_all()
        elif char == "±":
            self.toggle_sign()

    def handle_number(self, num):
        if self.reset_screen or self.current_input == "0":
            self.current_input = num
            self.reset_screen = False
        elif len(self.current_input.replace("-", "").replace(".", "")) < 15:
            self.current_input += num
        self.update_display(self.current_input)

    def handle_decimal(self):
        if self.reset_screen:
            self.current_input = "0."
            self.reset_screen = False
        elif "." not in self.current_input:
            self.current_input += "."
        self.update_display(self.current_input)

    def handle_operator(self, op):
        if self.operator and not self.reset_screen:
            self.calculate_result()
            if self.error:
                return
        self.previous_input = self.current_input
        self.operator = op
        self.reset_screen = True

    def calculate_result(self):
        if not self.operator or self.previous_input == "":
            return
        try:
            a = float(self.previous_input)
            b = float(self.current_input)

            if self.operator == "+":
                res = a + b
            elif self.operator == "-":
                res = a - b
            elif self.operator == "*":
                res = a * b
            else:
                if b == 0:
                    self.show_error("Cannot divide by 0")
                    return
                res = a / b

            if res.is_integer():
                self.current_input = str(int(res))
            else:
                self.current_input = str(round(res, 6))

            self.update_display(self.current_input)
            self.previous_input = ""
            self.operator = ""
            self.reset_screen = True
        except Exception:
            self.show_error("Error")

    def show_error(self, message):
        self.reset_state()
        self.error = True
        self.update_display(message)

    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.update_display(self.current_input)

    def backspace(self):
        if self.reset_screen or len(self.current_input) <= 1 or (
            len(self.current_input) == 2 and self.current_input.startswith("-")
        ):
            self.current_input = "0"
        else:
            self.current_input = self.current_input[:-1]
        self.update_display(self.current_input)

    def clear_all(self):
        self.reset_state()
        self.update_display("0")

    def reset_state(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.reset_screen = False
        self.error = False

    def update_display(self, text):
        n = len(text)
        size = 26 if n <= 9 else 22 if n <= 12 else 19 if n <= 16 else 15
        self.display_font.configure(size=size)
        self.canvas.itemconfig(self.display_id, text=text)

    # ------------------------------------------------------------------
    # Keyboard
    # ------------------------------------------------------------------
    def key_press(self, event):
        key = event.char
        if key and key in "0123456789":
            self.on_button_click(key)
        elif key == ".":
            self.on_button_click(".")
        elif key in ("+", "-", "*", "/"):
            self.on_button_click(key)
        elif event.keysym in ("Return", "KP_Enter", "equal"):
            self.on_button_click("=")
        elif event.keysym == "Escape":
            self.clear_all()
        elif event.keysym == "BackSpace":
            if self.error:
                self.clear_all()
            else:
                self.backspace()


if __name__ == "__main__":
    app = PinkCalculator()
    app.mainloop()