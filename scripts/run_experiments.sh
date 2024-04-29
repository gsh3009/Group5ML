# generate datasets
# DO NOT RUN THIS SCRIPT YET!!!!
bash scripts/generate_data.sh

# train with number of epochs and run_id
python python/train.py data/train/sr5 --n_epochs 10 --run_id 100

# test on given directory using restore_id, epoch, and amount of rounds to run tests on
python python/test.py data/test/sr5 100 9 10

# solve problems using solver given directory, restore_id, epoch and amount of rounds
python python/solve.py data/test/sr5 100 9 10