# Image sequence to GIF converter

This program converts an image sequence into a transparent GIF.
There are two modes of this program, each having its own file:
- ``export_many.py`` or `export_many_img_sequences.bat`
- ``export_single.py`` or `export_one_image_sequence.bat`

This program is best paired with [this one](https://github.com/i-winxd/FnF-Spritesheet-to-PNG-seq)
though you can use this independently.

## Dependencies

Read this or your program may not work!!

You need Python 3.10 installed on your computer. You
should download it from the official Python site.

You also need
`Pillow`. You can install `Pillow` by running this in your
command prompt:

```commandline
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

Depending on your Python installation, you
may need to replace `python3` with `py` or `python`.
Please make sure you didn't install Python from the
Windows 10 Store, because it messes things up. Alternatively,
this command may work:

`pip install Pillow`

# Running the program

Download this code by going to `code` and clicking "download zip".

**This program SHOULD work on macOS and Linux, but
I have not tested it there.** On Windows, make sure
you do not run this through the start menu 
(the program will crash). The program will only work if
you run it through the same current working directory as the
`.py` files are in.

This program can't delete any files, but it does overwrite
existing files if needed, ONLY in the export folder.

This program has two modules.

## Export many

How to run: click on `export_many_img_sequences.bat`.
Running this will prompt you to open a folder, which contains
folders of image sequences. It will create GIFs of all folders that
appear to be image sequences (all files in the folder look
like `[...]####.png` - or more precisely, have the regex `^.+\d+\.png$`)

All GIFs will be exported in a folder named `export`, which is relative
to your current working directory (the folder you're running this from).
If you click on the bat, the current working directory is
the folder this BAT file is in.

## Export single

How to run: click on `export_one_img_sequence.bat`. You will
be prompted to select a folder that is an image sequence. It
works very similarly to export many, but only targets
one image sequence.

Note for both modes: The export folder will not have any sub-folders.
All GIFs will be dumped there. You are expected to empty the folder
yourself.

## Preferences

Modify this `.json` file if you want.
- `fps` is self-explanatory. This is the FPS for the GIF that
will be exported by this program. Default is 24. The program crashes
if the FPS is 0 or lower. Decimal FPS values are not supported and the
program will always round down if you specify a decimal FPS.

- `frames` is the number of frames this program will try to export for
each GIF. You should only set a positive value for this if you only
plan on exporting one image sequence. This value freezes the last frame of the GIF
until the GIF has `frames` many frames, or shortens the GIF such that it can't
have more frames than `frames`. If negative, then each GIF will have as many frames
as the number of PNGs in the PNG sequence. If 0, this value is set to 1. Default is 24.

**IMPORTANT WARNING:** Don't make any assumptions about the duration of the GIF
based on the values you set for `fps` and `frames`. The duration of any exported GIF
tends to be very unsteady. If you want a GIF to loop as quickly as a beat of a song,
you're better off replicating that in another software.
