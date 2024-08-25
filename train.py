#script for fine-tuning Conformer CTC model

#loading the model

import nemo.collections.asr as nemo_asr
from nemo.utils import logging, exp_manager
import copy
from omegaconf import OmegaConf, open_dict


asr_model = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="stt_es_conformer_ctc_large")

TOKENIZER_DIR = "/home/mourb/nemo/train/tokenizer_spe_bpe_v1024"
asr_model.change_vocabulary(new_tokenizer_dir=TOKENIZER_DIR, new_tokenizer_type="bpe")
     
## Checking parameters of pretrained model
# params = OmegaConf.load("conformer_ctc_bpe.yaml")
# print(OmegaConf.to_yaml(params))


#setup data loaders
cfg = copy.deepcopy(asr_model.cfg)
# print(cfg.decoding)

#removing SpecAugment
# cfg.spec_augment.freq_masks = 0
# cfg.spec_augment.time_masks = 0


# setting up tokenizers
cfg.tokenizer.dir = TOKENIZER_DIR
cfg.tokenizer.type = "bpe"
asr_model.cfg.tokenizer = cfg.tokenizer

''' to preserve the parameters of the pretrained decoder uncomment 
'''

# pretrained_decoder = asr_model.decoder.state_dict()
# if asr_model.decoder.decoder_layers[0].weight.shape == pretrained_decoder['decoder_layers.0.weight'].shape:
#     asr_model.decoder.load_state_dict(pretrained_decoder)
#     logging.info("Decoder shapes matched - restored weights from pre-trained model")
# else:
#     logging.info("\nDecoder shapes did not match - could not restore decoder weights from pre-trained model.")


#setting up data loaders
# print(OmegaConf.to_yaml(cfg.decoder))


with open_dict(cfg):
    
    #train dataset
    cfg.train_ds.manifest_filepath = "./train/train_manifest.json"
    cfg.train_ds.batch_size = 8
    cfg.train_ds.num_workers = 8
    cfg.train_ds.pin_memory = True
    cfg.train_ds.use_start_end_token = True
    cfg.train_ds.trim_silence = True
    cfg.train_ds.is_tarred = False
    cfg.train_ds.augmentor = None
    # cfg.train_ds.augmentor.noise.audio_tar_filepaths = False


    # validation dataset
    cfg.validation_ds.manifest_filepath = "./dev/dev_manifest.json"
    cfg.validation_ds.batch_size = 8
    cfg.validation_ds.num_workers = 8
    cfg.validation_ds.pin_memory = False
    cfg.validation_ds.use_start_end_token = True
    cfg.validation_ds.trim_silence = True

    # test dataset

    
asr_model.setup_training_data(cfg.train_ds)
asr_model.setup_validation_data(cfg.validation_ds)


    #optimizer and scheduler
with open_dict(asr_model.cfg.optim):
    asr_model.cfg.optim.lr = 0.02
    asr_model.cfg.optim.weight_decay = 0.001
    # asr_model.cfg.sched.name = 'CosineAnnealing'
    asr_model.cfg.optim.sched.warmup_steps = 20000  # Remove default number of steps of warmup
    asr_model.cfg.optim.sched.warmup_ratio = None  # 10 % warmup
    asr_model.cfg.optim.sched.min_lr = 1e-8

# # asr_model.setup_optimization = model.from_config_dict(model.cfg.spec_augment)

# #training with pl and logging using wandb
import torch
import pytorch_lightning as ptl
# from pytorch_lightning.loggers import WandbLogger




# wandb_logger = WandbLogger(project="ConformerCTC")
# wandb_logger.log_hyperparams(vars(cfg.train_ds))
# wandb_logger.log_hyperparams(vars(cfg.validation_ds))
# cfg_dict = OmegaConf.to_container(cfg)
# wandb_logger.log_hyperparams(vars(cfg_dict))
# print("trainer config", OmegaConf.to_yaml(cfg))
# print("exp_manager config", OmegaConf.to_yaml(cfg.exp_manager))

# print(cfg.trainer)

trainer = ptl.Trainer(devices=-1,
                      accelerator='gpu',
                      strategy='ddp',
                      max_epochs=50,
                      accumulate_grad_batches=1,
                      enable_checkpointing=False,
                      logger=False,
                      log_every_n_steps=5,
                      check_val_every_n_epoch=5)


'''for wandb_logging uncomment below. Using MLFlow for this training'''
# exp_manager.create_wandb_logger=True
# exp_manager.wandb_logger_kwargs.name="CONFORMER CTC Spanish"
# exp_manager.wandb_logger_kwargs.project="Training"



#create MLFlow logger 
config = exp_manager.ExpManagerConfig(exp_dir="./Conformer_Spanish", name="CONFORMER_large_es_to_spanish", 
        create_checkpoint_callback=True, 
        create_tensorboard_logger=False,
        checkpoint_callback_params=exp_manager.CallbackParams(
        monitor="val_wer",
        mode="min",
        always_save_nemo=True,
        save_best_model=True,
    ), resume_if_exists=True,
    resume_ignore_no_checkpoint=True,
    create_mlflow_logger = True, mlflow_logger_kwargs=exp_manager.MLFlowParams(experiment_name="CONFORMER_es_large"))
config = OmegaConf.structured(config)
logdir = exp_manager.exp_manager(trainer, config)



asr_model.set_trainer(trainer)
asr_model.cfg = asr_model._cfg
trainer.fit(asr_model)
asr_model.save_to("Conformer_es_large.nemo")




