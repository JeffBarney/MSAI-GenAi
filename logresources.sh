#!/bin/sh
#SBATCH --account=p32562
#SBATCH --partition=gengpu
#SBATCH --gres=gpu:a100:1
#SBATCH --time=00:10:00 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --output=/home/nee0873/resources.log

module purge
eval "$(conda shell.bash hook)"
# conda activate /home/sil3812/.conda/envs/genai I'm not sure what to do here

python log_resources.py