import os
import re
from tinytag import TinyTag
from tqdm import tqdm


def clean_playlist(input_m3u, output_m3u, max_length_minutes=15):
    max_length_seconds = max_length_minutes * 60

    # Set to keep track of what we've already added
    seen_tracks = set()
    filtered_songs = []

    # Regular expression to catch common "live" tagging conventions
    # without catching words that just happen to contain "live"
    live_pattern = re.compile(r'\(live|\[live|- live|live at|live version|live in', re.IGNORECASE)

    print(f"Reading paths from '{input_m3u}'...")

    # Read the M3U, ignoring empty lines and the #EXTM3U header
    with open(input_m3u, 'r', encoding='utf-8') as f:
        file_paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not file_paths:
        print("The input playlist is empty or could not be read.")
        return

    print(f"Found {len(file_paths)} tracks in playlist. Applying filters...")

    for path in tqdm(file_paths, desc="Filtering tracks", unit="file", dynamic_ncols=True):
        # Skip if the file was moved or deleted
        if not os.path.exists(path):
            continue

        try:
            tag = TinyTag.get(path)

            # Filter 1: Over 15 minutes long
            if tag.duration and tag.duration > max_length_seconds:
                continue

            # Grab metadata, falling back to the filename if the title tag is missing
            title = tag.title or os.path.splitext(os.path.basename(path))[0]
            artist = tag.artist or "Unknown Artist"
            album = tag.album or ""

            # Filter 2: Live performances (checking both title and album name)
            if live_pattern.search(title) or live_pattern.search(album):
                continue

            # Filter 3: Duplicates
            # We strip whitespace and convert to lowercase so slight
            # capitalization differences don't bypass the filter
            track_key = (artist.strip().lower(), title.strip().lower())

            if track_key in seen_tracks:
                continue

            # If the track survives all filters, record its key and keep the path
            seen_tracks.add(track_key)
            filtered_songs.append(path)

        except Exception:
            pass

    # Write the new, cleaned M3U
    with open(output_m3u, 'w', encoding='utf-8') as playlist_file:
        playlist_file.write("#EXTM3U\n")
        for song_path in filtered_songs:
            playlist_file.write(f"{song_path}\n")

    print(f"\nDone! Kept {len(filtered_songs)} tracks out of {len(file_paths)}.")
    print(f"Cleaned playlist saved as: '{output_m3u}'")


# --- Setup your variables here ---
INPUT_PLAYLIST = r"D:\Music\Killing Time, Waiting For The Train or Bus.m3u"
OUTPUT_PLAYLIST = r"D:\Music\Killing Time (Cleaned).m3u"

if __name__ == "__main__":
    clean_playlist(INPUT_PLAYLIST, OUTPUT_PLAYLIST, max_length_minutes=15)