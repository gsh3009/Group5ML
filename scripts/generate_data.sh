rm -rf data/train/sr5
rm -rf data/train/EC
rm -rf data/test/sr5
rm -rf data/test/EC
mkdir -p data/train/sr5
mkdir -p data/train/EC
mkdir -p data/test/sr5
mkdir -p data/test/EC

for i in {1..2}; do
rm -rf dimacs/train/sr5/grp$i
mkdir -p dimacs/train/sr5/grp$i
rm -rf dimacs/test/sr5/grp$i
mkdir -p dimacs/test/sr5/grp$i

python python/gen_sr_dimacs.py dimacs/train/sr5/grp$i 100 --min_n 10 --max_n 40
python python/dimacs_to_data.py dimacs/train/sr5/grp$i data/train/sr5 60000
python python/gen_sr_dimacs.py dimacs/test/sr5/grp$i 100 --min_n 40 --max_n 40
python python/dimacs_to_data.py dimacs/test/sr5/grp$i data/test/sr5 60000
done;
rm -rf dimacs/train/EC/grp3EC
mkdir -p dimacs/train/EC/grp3EC
rm -rf dimacs/test/EC/grp3EC
mkdir -p dimacs/test/EC/grp3EC

python python/genEC_to_dimacs.py dimacs/train/EC/grp3EC/ --problem_size 40 --question_num 100
python python/genEC_to_dimacs.py dimacs/test/EC/grp3EC/ --problem_size 40 --question_num 100
python python/dimacs_to_data.py dimacs/train/EC/grp3EC data/train/EC 60000
python python/dimacs_to_data.py dimacs/test/EC/grp3EC data/test/EC 60000