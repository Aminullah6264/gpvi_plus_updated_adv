# Copyright (c) 2021 Horizon Robotics and ALF Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cProfile import label
import functools
import alf
from alf.utils import datagen
from alf.algorithms.hypernetwork_algorithm import HyperNetwork
from alf.trainers import policy_trainer

CONV_LAYER_PARAMS = (()) # These are empty becasue we configure ResNet in param_network.py file
FC_LAYER_PARAMS = ()     #


HIDDEN_LAYERS = (256, 512, 1024)

noise_dim = 256
batch_size = 256
# dcreator = functools.partial(datagen.load_cifar10, train_bs=batch_size, test_bs=256)

dcreator = functools.partial(datagen.load_cifar10,label_idx=[0,1,2,3,4,5], train_bs=batch_size, test_bs=batch_size)
dcreator_outlier = functools.partial(datagen.load_cifar10, label_idx=[6,7,8,9], train_bs=batch_size, test_bs=batch_size)

alf.config(
    'HyperNetwork',
    data_creator= dcreator,
    data_creator_outlier= dcreator_outlier,
    conv_layer_params=CONV_LAYER_PARAMS,
    fc_layer_params=FC_LAYER_PARAMS,
    use_conv_bias=False,
    use_conv_norm= 'en',  #'bn' , 'ln', 'en'
    use_fc_bias=False,
    use_fc_norm=None,
    hidden_layers=HIDDEN_LAYERS,
    noise_dim=noise_dim,
    num_particles=10,
    par_vi='svgd3',
    functional_gradient=True,
    loss_type='classification',
    init_lambda= 1,
    lambda_trainable=True,
    extra_noise_std= 1e-5,
    direct_jac_inverse=False,
    block_inverse_mvp=True,
    entropy_regularization= -1,
    inverse_mvp_hidden_size=512,
    inverse_mvp_hidden_layers=3,
    optimizer_lr = 1e-4,
    optimizer_wd= 5e-04,
    inverse_mvp_optimizer_lr= 1e-4,
    lambda_optimizer_lr = 1e-4,
    logging_training=True,
    logging_evaluate=True,
    attack = 'PGD',                 # PGD, FGSM, IFGSM, MIFGSM, RFGSM
    eps = 0.031, 
    eps_alpha = 0.007, 
    steps= 7,
    attackNorm = 'Linf',               # Linf, L2
    dataset='cifar10',                   # cifar10
    attacktype = 'WhiteBox',
    Adv_Training = False,           # Make it True, if you want to train it for Adv Attacks
    comment = 'Standard_ResNet_EN_Clean_Entropy-1'
    )                #WhiteBox #BlackBox

alf.config(
    'TrainerConfig',
    algorithm_ctor=HyperNetwork,
    ml_type='sl',
    num_iterations=300,
    num_checkpoints=1,
    evaluate=True,
    eval_uncertainty=True,
    eval_interval=1,
    summary_interval=1,
    debug_summaries=True,
    summarize_grads_and_vars=True,
    random_seed=0)
