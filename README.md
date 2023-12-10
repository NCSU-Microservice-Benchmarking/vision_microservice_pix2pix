## pix2pix
This project uses Python 3.11.7 (do not use 3.12.X or higher). See `requirements.txt` for other requirements.

Development steps involve training, then applying trained model to images+masks.

1. Download mask training data from https://apolloscape.auto/inpainting.html
1. Put image files as-is into `__pycache__/data/` and run `apply_masks.py` to prep the training data. This script applies white masks onto their associated images and sorts the unmasked/masked images into paired directories, `A` and `B`.
1. Follow [the training tips](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/a44f3f3a711578d1486f136596e0ecff8b4a56a8/docs/tips.md#prepare-your-own-datasets-for-pix2pix) to merge for training. (You might need to use the `--no_multiprocessing` option when running `combine_A_and_B.py`.)
1. [Trained](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix#pix2pix-traintest) the improved (GH: junyanz) pix2pix model:
    1. Clone repo and run `pip install -r requirements.txt` to ensure all packages are installed
    1. Install PyTorch with CUDA support for much faster training on the GPU: [`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`](https://pytorch.org/get-started/locally/)
    1. Run `python -m visdom.server` to visualize training
    1. Run in repo root `python train.py --dataroot path/to/data --name inpainting_pix2pix --model pix2pix --direction BtoA --netG resnet_6blocks --display_winsize 512 --load_size 512 --preprocess crop --crop_size 512 --batch_size 4`
    1. Wait and watch at http://localhost:8097/
1. Use trained model.

(Command used for testing model is `--preprocess none`)

To start the server, run `app.py`. See `requirements.txt`.

Test by running `send_request.py`, or running `curl -F image=@sample-image.png -F mask=@sample-mask.png --output result.png -X POST http://127.0.0.1:5000`, then checking `result.png`. 
