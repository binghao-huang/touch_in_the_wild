import subprocess
import sys
import os
import tempfile
import shutil

def compress_video(infile):
    if not os.path.isfile(infile):
        print(f"File not found: {infile}")
        return

    print(f"Compressing {infile}...")

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmpfile = tmp.name

    # Build ffmpeg command
    command = [
        "ffmpeg", "-i", infile,
        "-vcodec", "libx264",
        "-preset", "medium",
        "-crf", "23",               # less compression, better quality
        # "-vf", "scale=iw/1.5:-2", # optionally reduce size slightly
        "-acodec", "aac",
        "-b:a", "128k",             # better audio quality
        tmpfile
    ]

    try:
        subprocess.run(command, check=True)
        shutil.move(tmpfile, infile)
        print(f"Replaced original with compressed version: {infile}")
    except subprocess.CalledProcessError as e:
        print(f"Compression failed for {infile}: {e}")
        if os.path.exists(tmpfile):
            os.remove(tmpfile)

def main():
    if len(sys.argv) < 2:
        print("Usage: python compress_and_replace.py <video1> [video2 ...]")
        sys.exit(1)

    for infile in sys.argv[1:]:
        compress_video(infile)

if __name__ == "__main__":
    main()
