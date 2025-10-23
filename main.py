import csv
import sys
from pathlib import Path
import shutil
import os

REQUESTER_FIELD = "Name of Participant"
ASSIGNED_FIELD = "Assigned To"
SONG_FIELD = "Song Name"

INPUT_SONG_FOLDER_PATH = "input_song_folders"
OUTPUT_SONG_FOLDER_PATH = "output_song_folders"


def handle_song(giftee, gifter, song):
    in_path = Path(INPUT_SONG_FOLDER_PATH)/song
    if not in_path.is_dir():
        print(f"ERROR: Source directory for song {song} not present or misnamed\nSkipping...\n")
        return
    files = os.listdir(in_path)
    # Expect directory to have two files only, exactly one of which is a .sm/.ssc file
    if not (len(files) == 2 and sum((".sm" in filename or ".ssc" in filename) for filename in files) == 1):
        print(f"ERROR: Source directory for song {song} does not include exactly one .sm/.ssc file!\nSkipping...\n")
        return
    # TODO: Other sanity checks here? Perhaps whether there's a song-like file present, etc

    out_path = Path(OUTPUT_SONG_FOLDER_PATH)/f"to {giftee} - {song} ({gifter})"
    shutil.copytree(src=in_path, dst=out_path)

    chart_file = ''.join([filename if (".sm" in filename or ".ssc" in filename) else "" for filename in files]) # This is a stupid way to do it but I'm lazy
    
    # Continuing horrible things here
    orig_chart = ""
    with open(out_path/chart_file) as chart:
        orig_chart = chart.read()
    
    if orig_chart.count("#SUBTITLE:;") != 1:
        print(f"ERROR: Unable to set subtitle field of {song};\nSkipping...\n")
        return

    new_chart = orig_chart.replace("#SUBTITLE:;", f"#SUBTITLE:From {gifter} to {giftee};")
    with open(out_path/chart_file, 'tw') as chart:
        chart.write(new_chart)
    

def main():
    if len(sys.argv) != 2:
        print("Usage: `./main.py path_to_spreadsheet.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    with open(csv_path, newline='') as csvfile:
        secret_santa_info = csv.DictReader(csvfile, delimiter=',')
        for row in secret_santa_info:
            if row.get(REQUESTER_FIELD) is None or row.get(ASSIGNED_FIELD) is None or row.get(SONG_FIELD) is None:
                print(f"ERROR: {row}")
                continue
            handle_song(row.get(REQUESTER_FIELD), row.get(ASSIGNED_FIELD), row.get(SONG_FIELD))
            
                


if __name__ == "__main__":
    main()