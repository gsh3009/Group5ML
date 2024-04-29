# runs experiment on generated dataset of performance of model when lr_decay changes
count=1
for i in 0.1 0.5 0.99 ; do
    # train
    python3 python/train.py data/train/EC --n_epochs 10 --run_id 200$count --lr_decay $i
    # test
    python3 python/test.py data/test/EC 200$count 9 10 --lr_decay $i
    (count=count+1)
done;

echo "running control lr_decay=0.5"
python3 python/train.py data/train/sr5 --n_epochs 10 --run_id 200222 --lr_decay 0.5
python3 python/test.py data/test/sr5 200222 9 10 --lr_decay 0.5

echo "running control lr_decay=0.99"
python3 python/train.py data/train/sr5 --n_epochs 10 --run_id 200333 --lr_decay 0.99
python3 python/test.py data/test/sr5 200333 9 10 --lr_decay 0.99