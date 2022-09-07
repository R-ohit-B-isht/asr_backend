conda create --name check
conda activate check
conda install pytorch torchvision torchaudio cpuonly -c pytorch
conda install -c conda-forge transformers 
conda install -c conda-forge librosa 
python3 check.py