import tkinter as tk
from tkinter import messagebox
from predictor import HousePredictor

predictor = HousePredictor()

# ── Color palette ─────────────────────────────────────────────────────────────
BG        = "#0F1117"
CARD      = "#1A1D27"
BORDER    = "#2A2D3E"
ACCENT    = "#4F8EF7"
ACCENT2   = "#7C5CFC"
TEXT      = "#E8EAF0"
TEXT_MUTED= "#6B7280"
SUCCESS   = "#34D399"
ENTRY_BG  = "#252839"
FONT_MONO = ("Consolas", 10)
# ──────────────────────────────────────────────────────────────────────────────

root = tk.Tk()
root.title("Boston House Predictor")
root.geometry("480x620")
root.resizable(False, False)
root.configure(bg=BG)

# ── Utility: rounded rectangle on Canvas ──────────────────────────────────────
def round_rect(canvas, x1, y1, x2, y2, r=16, **kw):
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)

# ── Header ────────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=30, pady=(28, 6))

tk.Label(
    header, text="🏠", font=("Segoe UI Emoji", 28),
    bg=BG, fg=ACCENT
).pack(side="left", padx=(0, 10))

title_frame = tk.Frame(header, bg=BG)
title_frame.pack(side="left")

tk.Label(
    title_frame, text="Boston House",
    font=("Georgia", 20, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w")

tk.Label(
    title_frame, text="Price Predictor",
    font=("Georgia", 13, "italic"),
    bg=BG, fg=TEXT_MUTED
).pack(anchor="w")

divider = tk.Canvas(root, height=2, bg=BG, highlightthickness=0)
divider.pack(fill="x", padx=30, pady=(8, 0))
divider.create_line(0, 1, 480, 1, fill=BORDER, width=1)

# ── Card: Input fields ────────────────────────────────────────────────────────
card_canvas = tk.Canvas(root, bg=BG, highlightthickness=0, height=300)
card_canvas.pack(fill="x", padx=24, pady=(16, 0))

round_rect(card_canvas, 0, 0, 432, 295, r=14, fill=CARD, outline=BORDER, width=1)

card_inner = tk.Frame(card_canvas, bg=CARD)
card_canvas.create_window(216, 148, window=card_inner)

card_inner.columnconfigure(0, weight=1)

FIELDS = [
    ("RM — Average Rooms",     "e.g.  6.5",   "Number of rooms per dwelling"),
    ("LSTAT — % Lower Status", "e.g.  12.0",  "% of population with lower status"),
    ("PTRATIO — Pupil-Teacher","e.g.  18.0",  "Pupil-teacher ratio by town"),
]

entries = []

for i, (label, placeholder, hint) in enumerate(FIELDS):
    row = tk.Frame(card_inner, bg=CARD)
    row.grid(row=i, column=0, sticky="ew", padx=18, pady=(10, 0))

    tk.Label(row, text=label, font=("Segoe UI", 9, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w")

    tk.Label(row, text=hint, font=("Segoe UI", 7),
             bg=CARD, fg=TEXT_MUTED).pack(anchor="w")

    entry_frame = tk.Frame(row, bg=BORDER, bd=0)
    entry_frame.pack(fill="x", pady=(4, 0), ipady=1)

    entry = tk.Entry(
        entry_frame,
        font=FONT_MONO,
        bg=ENTRY_BG, fg=TEXT,
        insertbackground=ACCENT,
        relief="flat",
        bd=8,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
    )
    entry.pack(fill="x")
    entry.insert(0, placeholder)
    entry.config(fg=TEXT_MUTED)

    def _focus_in(e, ent=entry, ph=placeholder):
        if ent.get() == ph:
            ent.delete(0, "end")
            ent.config(fg=TEXT)

    def _focus_out(e, ent=entry, ph=placeholder):
        if not ent.get().strip():
            ent.insert(0, ph)
            ent.config(fg=TEXT_MUTED)

    entry.bind("<FocusIn>",  _focus_in)
    entry.bind("<FocusOut>", _focus_out)
    entries.append((entry, placeholder))

rm_entry, lstat_entry, ptratio_entry = entries

# ── Result display ────────────────────────────────────────────────────────────
result_outer = tk.Frame(root, bg=BG)
result_outer.pack(fill="x", padx=24, pady=(20, 0))

result_canvas = tk.Canvas(result_outer, bg=BG, highlightthickness=0, height=88)
result_canvas.pack(fill="x")

result_bg = round_rect(
    result_canvas, 0, 0, 432, 82, r=14,
    fill="#0D1F0F", outline="#1A3A1F", width=1
)

result_label = tk.Label(
    result_canvas,
    text="Predicted Price",
    font=("Segoe UI", 9), bg="#0D1F0F", fg=TEXT_MUTED
)
result_canvas.create_window(216, 24, window=result_label)

price_label = tk.Label(
    result_canvas,
    text="—",
    font=("Georgia", 26, "bold"),
    bg="#0D1F0F", fg=SUCCESS
)
result_canvas.create_window(216, 58, window=price_label)

# ── Predict button ────────────────────────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(fill="x", padx=24, pady=(16, 0))

def _get_val(entry_tuple):
    e, ph = entry_tuple
    v = e.get().strip()
    if v == ph or v == "":
        raise ValueError
    return float(v)

def predict_price():
    try:
        rm      = _get_val(rm_entry)
        lstat   = _get_val(lstat_entry)
        ptratio = _get_val(ptratio_entry)
    except ValueError:
        messagebox.showerror("Input Error", "Harap masukkan angka yang valid di semua field.")
        return

    price = predictor.predict(rm, lstat, ptratio)

    for color in [ACCENT, SUCCESS, SUCCESS]:
        price_label.config(fg=color)
        root.update()
        root.after(80)

    price_label.config(text=f"${price:,.0f}")
    result_label.config(text="Estimated Market Value (×1000 USD)")
    result_canvas.itemconfig(result_bg, fill="#0D2A12", outline="#2A6B35")

def on_enter(e): predict_btn.config(bg=ACCENT2)
def on_leave(e): predict_btn.config(bg=ACCENT)

predict_btn = tk.Button(
    btn_frame,
    text="  Predict Price  →",
    font=("Segoe UI", 11, "bold"),
    bg=ACCENT, fg="white",
    activebackground=ACCENT2, activeforeground="white",
    relief="flat", bd=0,
    cursor="hand2",
    padx=20, pady=12,
    command=predict_price,
)
predict_btn.pack(fill="x", ipady=2)
predict_btn.bind("<Enter>", on_enter)
predict_btn.bind("<Leave>", on_leave)

root.bind("<Return>", lambda e: predict_price())

# ── Footer ────────────────────────────────────────────────────────────────────
tk.Label(
    root,
    text="Model trained on the Boston Housing Dataset",
    font=("Segoe UI", 7), bg=BG, fg=TEXT_MUTED
).pack(pady=(14, 0))

root.mainloop()