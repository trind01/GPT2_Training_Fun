Using the [gpt-2 git repo](https://github.com/openai/gpt-2) and using the training and encoding files from [this repo](https://github.com/nshepperd/gpt-2)

## Set Up
To set this up.
```
python -m venv gpt_env
.\gpt_env\Scripts\activate
pip install requirements.txt
```

Then download a model:
```
python download_model.py 124M
```

A larger model can be used, but you gpu might not be able to handle it.

## Gather Data
To gather data you need to scrape data.
Every sample should be separated by "<End of Data>".
Use the gathering scripts for examples.

Once data is gathered run the command outside the src folder.

```
python ./src/encode.py iroh_quotes.txt ./src/iroh_quotes.npz
```


## Training
Run the command inside src:
```
python train.py --dataset iroh_quotes.npz
```

You can add parameters like
```
python train.py --dataset iroh_quotes.npz --learning_rate 0.0001 --top_p 0.9 --run_name iroh
```

You can also set the batch size, but if you are using a gpu you may run out of memory.
```
python train.py --dataset iroh_quotes.npz --batch_size 2
```

## Generating Samples
For unconditional:
```
python generate_unconditional_samples.py --temperature 0.8 --top_k 40 --model_name iroh
```

For conditional:
```
python interactive_conditional_samples.py --temperature 0.8 --top_k 40 --model_name iroh
```