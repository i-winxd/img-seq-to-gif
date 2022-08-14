import os
import re
from dataclasses import dataclass
import json
from PIL import Image
from tkinter import filedialog


@dataclass
class Prefs:
    fps: int  # frames per second
    frames: int  # forces the gif to have this many frames, or negative
    # if you don't want that


def make_export_folder(folder_name_path: str) -> None:
    """Attempts to make a new folder named folder_name.
    If it is already there, do nothing. Otherwise, make it."""
    assert "/" not in folder_name_path and "\\" not in folder_name_path
    exists = os.path.exists(folder_name_path)
    if not exists:
        os.makedirs(folder_name_path)


def check_all_valid_files(list_files: list[str]) -> bool:
    """Check that all the files in list_files is part of an
    image sequence
    """
    reg = re.compile(r'^.*\d+\.png$')
    # ensures that files are in the form [...]####.png
    for lf in list_files:
        if not re.fullmatch(reg, lf):
            return False
    return True


def extend_or_trim_list(cur_list: list[str], target_length: int) -> None:
    """Mutates cur_list, where:
        if target_length is lower than the length of cur_list, then
            this will result in cur_list[:target_length]
        otherwise, this will copy the last element of cur_list len(cur_list) - target_length
            times
    """
    if target_length == -1:
        return
    if len(cur_list) == 0:
        return
    if target_length > len(cur_list):
        last_element = cur_list[-1]
        for i in range(len(cur_list), target_length):
            cur_list.append(last_element)
    elif target_length < len(cur_list):
        for _ in range(len(cur_list) - 1, target_length - 1, -1):
            cur_list.pop()
    # assert len(cur_list) == target_length


def export_single(prefs: Prefs) -> None:
    """No recursive layer. Folder you're selecting
    is the folder with the image sequence"""
    make_export_folder("export")
    lfp = filedialog.askdirectory(title="Select a folder, which "
                                        "directly contains the image sequence").replace("\\", "/")
    folder_name = lfp[lfp.rfind("/") + 1:]
    assert "/" not in folder_name  # must be met at all times
    all_files = os.listdir(lfp)
    if not check_all_valid_files(all_files):
        print("The folder you selected didn't have a PNG sequence")
        return
    all_files_with_root = [lfp + "/" + sf for sf in all_files]
    fp_out = f"export/{folder_name}_export.gif"
    sorted_images = sorted(all_files_with_root, key=lambda s: s[s.rfind("/") + 1:])
    extend_or_trim_list(sorted_images, prefs.frames)
    seconds_per_frame = 1 / prefs.fps
    # OPEN AND SAVE IMAGES
    imgs = (Image.open(f) for f in sorted_images)
    img = next(imgs)  # extract first image from iterator
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=seconds_per_frame * 1000, loop=0, disposal=2)


def export_all(prefs: Prefs) -> None:
    """One recursive layer."""
    make_export_folder("export")
    # filepaths
    folder_selected = filedialog.askdirectory(title="Select a folder, which contains a "
                                                    "folder of image sequences").replace("\\", "/")
    print(folder_selected)
    subfolders = [f.path.replace("\\", "/") for f in os.scandir(folder_selected) if f.is_dir()]  # type: ignore
    print(subfolders)
    # the name of all subfolders, which
    # we don't really need
    for lfp in subfolders:
        folder_name = lfp[lfp.rfind("/") + 1:]
        assert "/" not in folder_name  # must be met at all times
        all_files = os.listdir(lfp)
        if not check_all_valid_files(all_files):
            print("Some folder didn't have a PNG sequence")
            continue
        all_files_with_root = [lfp + "/" + sf for sf in all_files]
        fp_out = f"export/{folder_name}_export.gif"
        sorted_images = sorted(all_files_with_root, key=lambda s: s[s.rfind("/") + 1:])
        seconds_per_frame = 1 / prefs.fps
        # OPEN AND SAVE IMAGES
        imgs = (Image.open(f) for f in sorted_images)
        img = next(imgs)  # extract first image from iterator
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                 save_all=True, duration=seconds_per_frame * 1000, loop=0, disposal=2)


def generate_prefs() -> Prefs:
    with open("preferences.json") as f:
        data: dict = json.load(f)
    fps_count = int(data.get('fps', 24))
    if fps_count <= 0:
        raise ValueError("FPS 0 or negative!!")
    frame_count = int(data.get('frames', -1))
    if frame_count == 0:
        frame_count += 1
    return Prefs(fps_count, frame_count)


if __name__ == '__main__':
    export_all(generate_prefs())
    print("finished!!")
