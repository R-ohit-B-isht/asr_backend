conda create --name check
conda activate check
conda install pytorch torchvision torchaudio cpuonly -c pytorch
conda install -c conda-forge transformers 
conda install -c conda-forge librosa 
conda install -c conda-forge ffmpeg
conda install -c conda-forge mp3splt
conda install -c conda-forge sox
conda install -c conda-forge libsox-fmt-mp3

python3 check.py