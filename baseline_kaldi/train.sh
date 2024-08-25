#stage 4 onwards of https://github.com/kaldi-asr/kaldi/blob/master/egs/tedlium/s5/run.sh


#steps/align_si.sh --nj 32 data/train data/lang exp/tri1 exp/tri1_ali

steps/train_lda_mllt.sh 2500 15000 data/train data/lang exp/tri1_ali exp/tri2

utils/mkgraph.sh data/lang exp/tri2 exp/tri2/graph



steps/decode.sh --nj 32 --num-threads 8 exp/tri2/graph data/dev_LDC exp/tri2/decode_dev
steps/decode.sh --nj 32 --num-threads 8 exp/tri2/graph data/test exp/tri2/decode_test


#stage 6 (skipping 5)

steps/align_si.sh --nj 32 data/train data/lang exp/tri2 exp/tri2_ali

steps/train_sat.sh 2500 15000 data/train data/lang exp/tri2_ali exp/tri3

utils/mkgraph.sh data/lang exp/tri3 exp/tri3/graph

steps/decode_fmllr.sh --nj 32 --num-threads 8 exp/tri3/graph data/test exp/tri3/decode_test

#step 7

steps/align_fmllr.sh --nj 32 data/train data/lang exp/tri3 exp/tri3_ali

steps/train_sat.sh 2500 15000 data/train data/lang exp/tri3_ali exp/tri4

utils/mkgraph.sh data/lang exp/tri4 exp/tri4/graph

steps/decode_fmllr.sh --nj 32 --num-threads 8 exp/tri4/graph data/test exp/tri4/decode_test


