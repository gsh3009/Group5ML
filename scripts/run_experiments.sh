# generate datasets
for ty in "train" "test" ; do
    rm -rf data/$ty/sr5
    mkdir -p data/$ty/sr5
    for i in {1..2}; do
	rm -rf dimacs/$ty/sr5/grp$i
	mkdir -p dimacs/$ty/sr5/grp$i
	python python/gen_sr_dimacs.py dimacs/$ty/sr5/grp$i 10 --min_n 10 --max_n 40
    done;
    rm -rf dimacs/$ty/sr5/grp3EC
    mkdir -p dimacs/$ty/sr5/grp3EC
    python python/genEC_to_dimacs.py dimacs/$ty/sr5/grp3EC/
    python python/dimacs_to_data.py dimacs/$ty/sr5/grp3EC data/$ty/sr5 60000
done;

# train with number of epochs and run_id
python python/train.py data/train/sr5 --n_epochs 10 --run_id 100

# test on given directory using restore_id, epoch, and amount of rounds to run tests on
python python/test.py data/test/sr5 100 9 10

# solve problems using solver given directory, restore_id, epoch and amount of rounds
python python/solve.py data/test/sr5 100 9 10