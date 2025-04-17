#!/bin/sh
#SBATCH --account=e32706
#SBATCH --partition=gengpu
#SBATCH --gres=gpu:a100:1
#SBATCH --time=00:10:00 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --output=/home/nee0873/resources.log

module purge
eval "$(conda shell.bash hook)"
conda activate /home/nee0873/.conda/envs/genai

python log_resources.py