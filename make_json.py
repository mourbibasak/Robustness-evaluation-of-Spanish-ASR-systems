import os
import json
import librosa

# Function to build a manifest
def build_manifest(wav_scp_path, text_path, manifest_path):
    with open(wav_scp_path, 'r') as wav_file, open(text_path, 'r') as text_file:
        with open(manifest_path, 'w') as fout:
            for wav_line, text_line in zip(wav_file, text_file):
                # Lines from wav.scp look like this:
                # file_id /path/to/audio/file.wav
                file_id, audio_path = wav_line.strip().split(' ', 1)

                # Lines from text file look like this:
                # file_id transcript
                transcript = text_line.strip().split(' ', 1)[1].lower()

                duration = librosa.core.get_duration(filename=audio_path)

                # Write the metadata to the manifest
                metadata = {
                    "audio_filepath": audio_path,
                    "duration": duration,
                    "text": transcript
                }
                json.dump(metadata, fout)
                fout.write('\n')

# Building Manifests
print("******")
# train_wav_scp = 'train/wav.scp'
# train_text = 'train/text'
# train_manifest = 'train/train_manifest.json'

# if not os.path.isfile(train_manifest):
#     build_manifest(train_wav_scp, train_text, train_manifest)
#     print("Training manifest created.")

# Repeat the process for the test set if needed
test_wav_scp = 'dev/wav.scp'
test_text = 'dev/text'
test_manifest = 'dev/test_manifest.json'
if not os.path.isfile(test_manifest):
    build_manifest(test_wav_scp, test_text, test_manifest)
    print("Dev manifest created.")

print("***Done***")
