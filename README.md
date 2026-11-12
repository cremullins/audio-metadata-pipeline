# Audio Metadata ETL Pipeline
A simple Python data pipeline I used to find songs under 10 minutes to listen to while waiting for a train.

## The problem
While waiting ten minutes for a late running train, I thought to myself how great it would be to have a playlist of songs that were between seven and ten minutes long on my Digital Audio Player (DAP), so I could load it up to find a track to pass the time.

I decided this would make a great Python project. Solving this problem presented challenges, such as duplicate files, unwanted live versions of studio tracks, and filtering out files that were too long for my needs.

## The solution
I built this local pipeline to:
* Extract metadata from audio files on my external storage drive using `tinytag`.
* Filter out duplicate tracks, live performances (using regular expressions), and tracks over 15 minutes long.
* Automate the transfer of existing album folders on my DAP's internal memory to the SD card using `shutil` and `os.walk`, with user-confirmation failsafes to prevent data loss. This prevented duplicate files from being created on the DAP's internal database when I transferred the playlist over using my computer's media player.

### Notes
My decision to include code that would print the file folders to be moved, as well as a Y/N confirmation, proved highly useful, as I noticed that an earlier version of the code wanted to move the entirety of my internal music library over to the SD card. I rewrote the code to ensure it would skip over "loose" files that would cause this problem, saving me a headache later on.
