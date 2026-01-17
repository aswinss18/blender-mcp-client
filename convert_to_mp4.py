"""
Convert PNG image sequence to MP4 video
Usage: python convert_to_mp4.py <input_folder> <output_file.mp4>
"""
import subprocess
import sys
import os
from pathlib import Path

def convert_images_to_mp4(input_folder, output_file, fps=24):
    """Convert a sequence of PNG images to MP4 video using ffmpeg"""
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: ffmpeg is not installed or not in PATH")
        print("\nTo install ffmpeg:")
        print("1. Download from: https://ffmpeg.org/download.html")
        print("2. Or use: winget install ffmpeg")
        print("3. Or use: choco install ffmpeg")
        return False
    
    # Find the pattern for input files
    input_pattern = os.path.join(input_folder, "*.png")
    
    # Check if files exist
    png_files = list(Path(input_folder).glob("*.png"))
    if not png_files:
        print(f"❌ Error: No PNG files found in {input_folder}")
        return False
    
    print(f"✅ Found {len(png_files)} PNG files")
    
    # Sort files to ensure correct order
    png_files.sort()
    first_file = png_files[0]
    
    # Determine the input pattern for ffmpeg
    # If files are named like frame_0001.png, frame_0002.png, etc.
    parent_dir = first_file.parent
    
    # Create a pattern - ffmpeg expects %04d for 4-digit numbers
    # We'll use a file list instead for more reliability
    file_list_path = parent_dir / "file_list.txt"
    with open(file_list_path, 'w') as f:
        for png_file in png_files:
            f.write(f"file '{png_file.name}'\n")
            f.write(f"duration {1/fps}\n")
    
    print(f"🎬 Converting to MP4 at {fps} fps...")
    
    # FFmpeg command
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(file_list_path),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '23',
        '-y',  # Overwrite output file
        str(output_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(parent_dir))
        
        if result.returncode == 0:
            print(f"✅ Video created successfully: {output_file}")
            print(f"📁 File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
            
            # Clean up file list
            file_list_path.unlink()
            return True
        else:
            print(f"❌ Error during conversion:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_to_mp4.py <input_folder> <output_file.mp4>")
        print("\nExample:")
        print("  python convert_to_mp4.py C:/tmp/umbrella C:/Users/aswin/Videos/umbrella.mp4")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_folder):
        print(f"❌ Error: Input folder does not exist: {input_folder}")
        sys.exit(1)
    
    success = convert_images_to_mp4(input_folder, output_file)
    sys.exit(0 if success else 1)
