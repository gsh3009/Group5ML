# runs experiment on generated dataset of performance of model when number of rounds changes

for i in 10 500 1000 ; do
    # train
    python python/train.py data/train/EC --n_epochs 10 --run_id 100$i
    # test
    python python/test.py data/test/EC 100$i 9 $i
    echo "$i done"
done;