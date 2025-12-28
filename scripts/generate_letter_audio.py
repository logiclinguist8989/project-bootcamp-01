"""
Script to generate letter pronunciation audio files using Google Text-to-Speech (gTTS).
This will create MP3 files for all 26 letters in the frontend/assets/audio/ directory.
"""

from gtts import gTTS
from pathlib import Path
import time

# Letter pronunciations
LETTER_PRONUNCIATIONS = {
    'A': 'ay',
    'B': 'bee',
    'C': 'see',
    'D': 'dee',
    'E': 'ee',
    'F': 'ef',
    'G': 'jee',
    'H': 'aych',
    'I': 'eye',
    'J': 'jay',
    'K': 'kay',
    'L': 'el',
    'M': 'em',
    'N': 'en',
    'O': 'oh',
    'P': 'pee',
    'Q': 'kyoo',
    'R': 'ar',
    'S': 'ess',
    'T': 'tee',
    'U': 'yoo',
    'V': 'vee',
    'W': 'double yoo',
    'X': 'eks',
    'Y': 'why',
    'Z': 'zee'
}

def generate_audio_files():
    """Generate MP3 audio files for all letter pronunciations."""
    # Get the audio directory path
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    audio_dir = project_root / 'frontend' / 'assets' / 'audio'
    
    # Create directory if it doesn't exist
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating letter pronunciation audio files...")
    print(f"Output directory: {audio_dir}\n")
    
    generated = 0
    failed = []
    
    for letter, pronunciation in LETTER_PRONUNCIATIONS.items():
        try:
            print(f"Generating {letter}.mp3 (pronunciation: '{pronunciation}')...", end=' ')
            
            # Create text-to-speech object
            tts = gTTS(text=pronunciation, lang='en', slow=False)
            
            # Save to file
            output_file = audio_dir / f"{letter}.mp3"
            tts.save(str(output_file))
            
            print("[OK]")
            generated += 1
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"[FAILED]: {e}")
            failed.append(letter)
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Generated: {generated}/26 files")
    if failed:
        print(f"  Failed: {', '.join(failed)}")
    else:
        print(f"  All files generated successfully!")
    print(f"{'='*50}")

if __name__ == '__main__':
    try:
        generate_audio_files()
    except ImportError:
        print("Error: gTTS library not found.")
        print("Please install it using: pip install gtts")
        print("\nOr add it to requirements.txt and run: pip install -r backend/requirements.txt")
    except Exception as e:
        print(f"Error: {e}")

