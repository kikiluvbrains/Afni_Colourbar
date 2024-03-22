import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

default_colors = ['#00ccff', '#0099ff', '#0069ff', '#0044ff', '#ff4400', '#ff6900', '#ffcc00', '#ffff00']

image_label = None
img_array = None

def generate_color_bar(width, height, vmin, vmax, text_size, text_color, colors):
    interpolated_colors = []
    for i in range(len(colors) - 1):
        cmap = mcolors.LinearSegmentedColormap.from_list('custom', [colors[i], colors[i + 1]], N=100)
        interpolated_colors.extend([cmap(i) for i in range(100)])
    cmap_custom = mcolors.ListedColormap(interpolated_colors, name='Custom')

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap=cmap_custom, norm=norm)
    sm.set_array([])

    fig, ax = plt.subplots(figsize=(width / 100, height / 100))
    cbar = plt.colorbar(sm, ticks=np.linspace(vmin, vmax, 9), orientation='horizontal', cax=ax)
    cbar.ax.xaxis.set_tick_params(color=text_color)
    cbar.outline.set_edgecolor(text_color)
    for text in cbar.ax.get_xticklabels():
        text.set_color(text_color)
        text.set_fontsize(int(text_size))

    ax.text(0, -0.2, f'{vmin}', transform=ax.transAxes, fontsize=int(text_size), color=text_color, ha='left', va='center')
    ax.text(1, -0.2, f'{vmax}', transform=ax.transAxes, fontsize=int(text_size), color=text_color, ha='right', va='center')

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.subplots_adjust(bottom=0.2)

    canvas = FigureCanvas(fig)
    canvas.draw()
    buf = np.asarray(canvas.buffer_rgba())
    plt.close(fig)
    return buf

def display_image(img_array, app):
    global image_label
    image = Image.fromarray(img_array)
    photo = ImageTk.PhotoImage(image=image)
    
    if image_label is not None:
        image_label.configure(image=photo)
    else:
        image_label = tk.Label(app, image=photo)
        image_label.pack()
    image_label.image = photo

def save_image():
    global img_array
    if img_array is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            image = Image.fromarray(img_array)
            image.save(file_path)
            print(f"Image saved to {file_path}")

def submit():
    global img_array
    colors = [entry.get() for entry in color_entries]
    width = float(width_entry.get())
    height = float(height_entry.get())
    vmin = float(vmin_entry.get())
    vmax = float(vmax_entry.get())
    text_size = text_size_var.get()
    text_color = text_color_var.get()
    img_array = generate_color_bar(width, height, vmin, vmax, text_size, text_color, colors)
    display_image(img_array, app)

app = tk.Tk()
app.title("Color Bar Generator")

color_entries = []
for i in range(8):
    tk.Label(app, text=f"Color {i+1}").pack()
    entry = tk.Entry(app)
    entry.insert(0, default_colors[i])
    entry.pack()
    color_entries.append(entry)

width_entry = tk.Entry(app)
width_entry.pack()
width_entry.insert(0, "800")

height_entry = tk.Entry(app)
height_entry.pack()
height_entry.insert(0, "100")

vmin_entry = tk.Entry(app)
vmin_entry.pack()
vmin_entry.insert(0, "-2.308")

vmax_entry = tk.Entry(app)
vmax_entry.pack()
vmax_entry.insert(0, "2.308")

text_size_var = tk.StringVar(app)
text_size_var.set("12")
tk.OptionMenu(app, text_size_var, "10", "12", "14").pack()

text_color_var = tk.StringVar(app)
text_color_var.set("black")
tk.OptionMenu(app, text_color_var, "black", "grey", "white").pack()

submit_button = tk.Button(app, text="Generate Color Bar", command=submit)
submit_button.pack()

save_button = tk.Button(app, text="Save Color Bar to File", command=save_image)
save_button.pack()

app.mainloop()
