import numpy as np
import pandas as pd
import glob
import toml
import librosa
import re

def read_config():
    """Read the config file."""
    config_file = 'config.toml'
    return toml.load(config_file)

def read_and_process_music(config):
    """Read all music files defined at config file and process them."""
    music_file_ext = config['music']['file_extension']
    music_folder = config['music']['source_folder']
    music_regex = re.compile(f"\s+\[.+\]\.{music_file_ext}")
    Data = []
    for music_path in glob.glob(music_folder + "/*." + music_file_ext ):
        music_name = music_regex.sub('', music_path[len(music_folder)+1:],1)
        [data, sampling_rate] = librosa.load(music_path)
        music_spectrum = librosa.stft(data)
        S = np.abs(music_spectrum)
        Data.append({'name': music_name, 'data': S})
    return Data
    
def save_processed_music(config, data):
    """Save the processed data to files."""
    save_folder = config['preprocess']['output_folder']
    for i in data:
        np.save(f"{save_folder}/{i['name']}", i['data'])



if __name__ == '__main__':
    config = read_config()
    D = read_and_process_music(config)
    save_processed_music(config, D)