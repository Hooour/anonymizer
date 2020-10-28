PYTHONPATH=$PYTHONPATH:. CUDA_VISIBLE_DEVICES=9 python anonymizer/bin/anonymize.py \
    --input ~/workspace/data_local/sl4_front_1.0/sl4_side_val_1.7.json \
    --image-output sl4_side_val_1.7 \
    --weights weights
