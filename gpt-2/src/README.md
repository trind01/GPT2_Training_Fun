Don't forget to go into virtual env

python train.py --dataset lil_sonic.npz --top_p 0.9 --batch_size 2

python generate_unconditional_samples.py --temperature 0.8 --top_k 40 --model_name lil_sonic