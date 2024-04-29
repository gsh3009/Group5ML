for i in 1 3 5 ; do
    # train
    python3 python/train.py data/train/EC --n_epochs 10 --run_id 300 --n_msg_layers $i
    # test
    python3 python/test.py data/test/EC 300 9 10 --n_msg_layers $i
done;

# run control
echo "running control... \n"

python3 python/train.py data/train/sr5 --n_epochs 10 --run_id 3001 --n_msg_layers 5
python3 python/test.py data/test/sr5 3001 9 10 --n_msg_layers 5