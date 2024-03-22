import tkinter as tk
from tkinter import colorchooser, ttk
from PIL import Image, ImageTk
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import win32clipboard
from io import BytesIO

default_colors = ['#00ccff', '#0099ff', '#0069ff', '#0044ff', '#ff4400', '#ff6900', '#ffcc00', '#ffff00']

# Initialize image_label and img_array as None
image_label = None
img_array = None

def generate_color_bar(width, height, vmin, vmax, text_size, text_color, colors):
    num_intervals = 8
    num_interpolated_colors = 100
    interpolated_colors = []
    for i in range(len(colors) - 1):
        cmap = mcolors.LinearSegmentedColormap.from_list('custom', [colors[i], colors[i + 1]], N=num_interpolated_colors)
        interpolated_colors.extend([cmap(i) for i in range(num_interpolated_colors)])
    cmap_custom = mcolors.ListedColormap(interpolated_colors, name='Custom')

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap=cmap_custom, norm=norm)
    sm.set_array([])

    fig, ax = plt.subplots(figsize=(width / 100, height / 100))
    cbar = plt.colorbar(sm, ticks=np.linspace(vmin, vmax, num_intervals+1), orientation='horizontal', cax=ax)
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

    # Adjust layout to make room for the bottom text
    plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin to make space for text labels

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

def copy_image_to_clipboard(img_array):
    output = BytesIO()
    image = Image.fromarray(img_array)
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def copy_to_clipboard():
    if img_array is not None:
        copy_image_to_clipboard(img_array)

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
    tk.Button(app, text="Choose", command=lambda entry=entry: colorchooser.askcolor(title="Choose color")[1]).pack()
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

copy_button = tk.Button(app, text="Copy Color Bar to Clipboard", command=copy_to_clipboard)
copy_button.pack()

app.mainloop()

