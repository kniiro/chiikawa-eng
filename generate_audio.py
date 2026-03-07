import csv
import os
import time
from gtts import gTTS

def main():
    csv_file = 'words.csv'
    output_dir = 'audio'
    upload_dir = 'audio_upload'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    print(f"Reading from {csv_file}")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        
        count = 0
        for row in reader:
            if not row or len(row) < 2:
                continue
                
            word = row[0].strip()
            
            # 安全なファイル名にする (スペースやスラッシュなどを置換、今回は英単語なので基本そのままでOK)
            safe_filename = word.replace(' ', '_').lower() + '.mp3'
            output_path = os.path.join(output_dir, safe_filename)
            
            # 既に存在する場合はスキップ
            if os.path.exists(output_path):
                print(f"Skipping {word} (already exists)")
                continue
                
            try:
                tts = gTTS(text=word, lang='en')
                tts.save(output_path)
                
                # Copy to upload dir
                upload_path = os.path.join(upload_dir, safe_filename)
                import shutil
                shutil.copy2(output_path, upload_path)
                
                print(f"Generated: {output_path} (copied to {upload_dir})")
                count += 1
                
                # API制限対策・行儀よくするために少しsleepする
                time.sleep(0.5)
            except Exception as e:
                print(f"Error generating {word}: {e}")
                
    print(f"Done! Generated {count} audio files.")

if __name__ == '__main__':
    main()
