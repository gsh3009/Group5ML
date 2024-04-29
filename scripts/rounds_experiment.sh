# runs experiment on generated dataset of performance of model when number of rounds changes
# results of test.py are compared for accuracy
for i in 10 500 1000 ; do
    # train
    python3 python/train.py data/train/EC --n_epochs 10 --run_id 100$i
    # test
    python3 python/test.py data/test/EC 100$i 9 $i
    echo "$i done"
done;

echo "running control rounds=500"
python3 python/train.py data/train/sr5 --n_epochs 10 --run_id 100222
python3 python/test.py data/test/sr5 100222 9 500