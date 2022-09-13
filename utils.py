import os
from dataclasses import fields


def model_from_dict(ModelName, arg_dict):
    fieldSet = {f.name for f in fields(ModelName) if f.init}
    filtered_dict = {k : v for k, v in arg_dict.items() if k in fieldSet}
    return ModelName(**filtered_dict)

# utility functions
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def make_folder_based_on_subject(subject):
    # make our boolean True, the email has "subject"
    has_subject = True
    # make a directory with the name of the subject
    folder_name = clean(subject)
    # we will also handle emails with the same subject name
    folder_counter = 0
    while os.path.isdir(folder_name):
        folder_counter += 1
        # we have the same folder name, add a number next to it
        if folder_name[-1].isdigit() and folder_name[-2] == "_":
            folder_name = f"{folder_name[:-2]}_{folder_counter}"
        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
            folder_name = f"{folder_name[:-3]}_{folder_counter}"
        else:
            folder_name = f"{folder_name}_{folder_counter}"
    os.mkdir(folder_name)
