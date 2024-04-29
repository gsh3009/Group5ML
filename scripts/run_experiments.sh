# runs all experiments
echo "> running rounds experiment..."
bash scripts/rounds_experiment.sh

echo "> running lr_decay experiment..."
bash scripts/lr_decay_experiments.sh

echo "> running msg_layer experiment..."
bash scripts/message_passing_layers.sh