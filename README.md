
# Afni Color Bar Generator

This program creates a color bar using default Afni hex values. Make sure to specify the minimum and maximum values for the bar plot. You can also adjust the color bar size, text size, and color. You may also select color values for the color bar if you do not intend to use the default color values from Afni. 

## If you would like to download one of our releases go to this link. we have applications for windows, mac and linux.
https://github.com/kikiluvbrains/Afni_Colourbar/releases

## The following guide is if you would like to generate an application for your personal system

Make sure to use the python scripts and dependencies that is compatible with your system, when following this guide.

for Mac/Linux: https://github.com/kikiluvbrains/Afni_Colourbar/tree/main/Colourbar_forMac
for Windows: 

### License

MIT License. Free to use.

#### Setup

Ensure Python is installed on your system. This application has been tested on Python 3.8+.

#### Dependencies

Install the required dependencies by running:

```
pip install -r requirements.txt
```

#### Compiling with PyInstaller

To create a standalone executable:

```
pyinstaller --onefile --windowed Colourbar_afni.py
```

### Usage

Run the compiled application directly, or execute the script using:

```
python Colourbar_afni.py
```

Follow the GUI prompts to generate and save your color bar.
