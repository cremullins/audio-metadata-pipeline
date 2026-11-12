import os
import shutil
from tinytag import TinyTag
from tqdm import tqdm


def get_target_albums(m3u_path):
    target_albums = set()
    print(f"Reading target albums from '{m3u_path}'...")

    with open(m3u_path, 'r', encoding='utf-8') as f:
        file_paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for path in tqdm(file_paths, desc="Extracting album data", unit="track", dynamic_ncols=True):
        if os.path.exists(path):
            try:
                tag = TinyTag.get(path)
                artist = (tag.artist or "Unknown Artist").strip().lower()
                album = (tag.album or "Unknown Album").strip().lower()

                if album != "unknown album":
                    target_albums.add((artist, album))
            except Exception:
                pass

    return target_albums


def move_albums_to_sd(internal_dir, sd_dir, target_albums):
    valid_extensions = ('.mp3', '.flac', '.m4a', '.wav', '.ogg', '.wma')
    folders_to_move = set()

    # Normalize the top-level path so we can safely compare it later
    internal_root = os.path.normpath(internal_dir)

    print("\nScanning internal memory for matching albums...")

    for root, _, files in os.walk(internal_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                try:
                    tag = TinyTag.get(file_path)
                    artist = (tag.artist or "").strip().lower()
                    album = (tag.album or "").strip().lower()

                    if (artist, album) in target_albums:
                        # CRUCIAL FIX: Ensure the folder we are flagging isn't the root directory
                        if os.path.normpath(root) != internal_root:
                            folders_to_move.add(root)
                        else:
                            print(f"\n[!] Skipped loose track '{file}' to prevent moving the root directory.")
                        break  # Move to the next directory
                except Exception:
                    continue

    if not folders_to_move:
        print("No matching albums found on the internal memory.")
        return

    print(f"\nFound {len(folders_to_move)} album folders to move:\n")

    for folder in folders_to_move:
        print(f" - {os.path.basename(folder)}")

    user_input = input(f"\nAre you sure you want to move these {len(folders_to_move)} folders to the SD card? (Y/N): ")

    if user_input.strip().lower() != 'y':
        print("\nOperation cancelled. No files were moved.")
        return

    print("\nProceeding with file transfer...")

    for folder_path in tqdm(folders_to_move, desc="Moving albums", unit="folder", dynamic_ncols=True):
        folder_name = os.path.basename(folder_path)
        destination_path = os.path.join(sd_dir, folder_name)

        try:
            if not os.path.exists(destination_path):
                shutil.move(folder_path, destination_path)
            else:
                print(f"\nSkipped '{folder_name}': Already exists on SD card.")
        except Exception as e:
            print(f"\nError moving '{folder_name}': {e}")

    print("\nOperation complete!")


# --- Setup your variables here ---
CLEANED_PLAYLIST = r"D:\Music\Killing Time (Cleaned).m3u"
INTERNAL_MEMORY_PATH = r"F:\MUSIC"
SD_CARD_PATH = r"H:\MUSIC"

if __name__ == "__main__":
    target_albums = get_target_albums(CLEANED_PLAYLIST)

    if target_albums:
        move_albums_to_sd(INTERNAL_MEMORY_PATH, SD_CARD_PATH, target_albums)
    else:
        print("No album data could be extracted from the playlist.")