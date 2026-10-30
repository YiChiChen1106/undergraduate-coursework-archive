set nnUNet_preprocessed=F:\shiwangmo\nnUNetFrame\nnUNet_preprocessed
set nnUNet_raw=F:\shiwangmo\nnUNetFrame\nnUNet_raw
set nnUNet_results=F:\shiwangmo\nnUNetFrame\nnUNet_results

export nnUNet_raw="/mnt/hdd/users/cychi/bishe/nnUNetFrame/nnUNet_raw"
export nnUNet_preprocessed="/mnt/hdd/users/cychi/bishe/nnUNetFrame/nnUNet_preprocessed"
export nnUNet_results="/mnt/hdd/users/cychi/bishe/nnUNetFrame/nnUNet_results"

nnUNetv2_train 501 2d 0 -tr my_train_150
nnUNetv2_predict -i F:\shiwangmo\drive -o F:\shiwangmo\drive-prediction -d 501 -c 2d -f 0 -tr my_train_150 -chk checkpoint_best.pth
nnUNetv2_predict -i F:\shiwangmo\drive-clahe -o F:\shiwangmo\drive-clahe_prediction -d 502 -c 2d -f 0 -tr my_train_150 -chk checkpoint_best.pth
nnUNetv2_train 502 2d 0 -tr MyTrainer_DiceFocal
nnUNetv2_predict -i F:\shiwangmo\drive-clahe -o F:\shiwangmo\drive-clahe-focal100-prediction -d 502 -c 2d -f 0 -tr MyTrainer_DiceFocal -chk checkpoint_best.pth
nnUNetv2_plan_and_preprocess -d 505 --verify_dataset_integrity
# 跑第 0 折
nnUNetv2_train 505 2d 0 -tr my_train_150

# 跑第 1 折
nnUNetv2_train 505 2d 1 -tr my_train_150

# 跑第 2 折
nnUNetv2_train 505 2d 2 -tr my_train_150

# 跑第 3 折
nnUNetv2_train 505 2d 3 -tr my_train_150

# 跑第 4 折
nnUNetv2_train 505 2d 4 -tr my_train_150

nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d 505 -c 2d -f 0 --save_probabilities0000000000000000000

nnUNetv2_train 505 2d 0 -tr nnUNetTrainerPANet

nnUNetv2_train 505 2d 4 -tr nnUNetTrainerPANet_LPT

nnUNetv2_train 505 2d 0 -tr nnUNetTrainerPANet_AFFM_NoDS