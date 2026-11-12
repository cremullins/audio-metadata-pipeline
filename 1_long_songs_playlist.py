import os
from tinytag import TinyTag
from tqdm import tqdm


def create_long_songs_playlist(music_dir, playlist_filename, min_length_minutes=7):
    min_length_seconds = min_length_minutes * 60

    if not playlist_filename.endswith('.m3u'):
        playlist_filename += '.m3u'

    playlist_path = os.path.join(music_dir, playlist_filename)
    long_songs = []
    valid_extensions = ('.mp3', '.flac', '.m4a', '.wav', '.ogg', '.wma')

    print(f"Scanning directory tree in '{music_dir}'...")

    # Pass 1: Quickly gather all valid audio files to get a total count
    audio_files = []
    for root, _, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                audio_files.append(os.path.join(root, file))

    if not audio_files:
        print("No audio files found in the specified directory.")
        return

    print(f"Found {len(audio_files)} audio files. Checking track lengths...")

    # Pass 2: Check durations with a dynamic progress bar
    # tqdm wraps the list and automatically prints/updates the bar in the console
    for file_path in tqdm(audio_files, desc="Processing tracks", unit="file", dynamic_ncols=True):
        try:
            tag = TinyTag.get(file_path)
            if tag.duration and tag.duration > min_length_seconds:
                long_songs.append(file_path)
        except Exception:
            # Silently pass errors (like corrupted files) so it doesn't break the progress bar visual
            pass

    # Write the M3U playlist file
    if long_songs:
        with open(playlist_path, 'w', encoding='utf-8') as playlist_file:
            playlist_file.write("#EXTM3U\n")
            for song_path in long_songs:
                playlist_file.write(f"{song_path}\n")

        print(f"\nSuccess! Created '{playlist_filename}' with {len(long_songs)} tracks.")
    else:
        print("\nNo songs found matching the criteria.")


# --- Setup your variables here ---
# Replace with the actual path to your music folder
MUSIC_DIRECTORY = r"D:\Music"
# Choose your custom playlist title
PLAYLIST_TITLE = "Killing Time, Waiting For The Train or Bus"

if __name__ == "__main__":
    create_long_songs_playlist(MUSIC_DIRECTORY, PLAYLIST_TITLE, min_length_minutes=7)