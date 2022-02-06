import os
import datetime
import time

from OpenKE import models
from OpenKE import config
import tensorflow as tf
from tensorboard.plugins.hparams import api as hp

from support_function import produce_name, get_parameters, get_model


# print(tf.__version__)


# Remove TF info and warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


epoch = 50000
model_name = "TransE"
alpha = 0.001
relation_dimension = 10
entity_dimension = 100
margin = 1
ent_neg_rate = 1
rel_neg_rate = 0
number_batch = 75
optimization_method = "SGD"

model = get_model(model_name)

input_path = "../KnowledgeGraph/"
output_path = "../Result_Embedding/"
cuda_device = "0"
export_step = 5
number_threads = 8
test = True


start_time = time.time()

name = produce_name(epoch=epoch, model=model, alpha=alpha, relation_dimension=relation_dimension,
                    entity_dimension=entity_dimension, margin=margin, ent_neg_rate=ent_neg_rate,
                    rel_neg_rate=rel_neg_rate, number_batch=number_batch, optimization_method=optimization_method)

dict_parameter = get_parameters(name)
for key in dict_parameter.keys():
    print(key, ": ", dict_parameter[key])

# Which GPU should be used
os.environ['CUDA_VISIBLE_DEVICES'] = cuda_device

con = config.Config()

con.set_in_path(input_path)
# Model parameters will be exported to json files automatically.
con.set_out_files(output_path + name + ".embedding.vec.json")
# Models will be exported via tf.Saver() automatically.
con.set_export_files(output_path + name + ".model.vec.tf")
con.set_export_steps(export_step)


con.set_work_threads(number_threads)

# Number of Epoch
con.set_train_times(epoch)

# Parameters
con.set_nbatches(number_batch)  # Number of batches to divide the train set
con.set_alpha(alpha)  # Learning rate
con.set_margin(margin)  # Margin for margin-based ranking loss

# Embedding dimensions
con.set_rel_dimension(relation_dimension)
con.set_ent_dimension(entity_dimension)
# con.set_dimension(dimension)  # This one sets both of them

# Corruption
con.set_bern(0)  # unif (bern = 0) or bern (bern = 1)
con.set_ent_neg_rate(ent_neg_rate)  # Per ogni positive triple quante entity corrotte creo
con.set_rel_neg_rate(rel_neg_rate)

# Optimization Method
con.set_opt_method(optimization_method)  # Adagrad Adadelta Adam SGD

if test:
    con.set_test_link_prediction(True)  # Test flag has to be set after all the other config

# Initialize experimental settings.
con.init()

# Set the knowledge embedding model
con.set_model(model)

# Train the model.
con.run()

if test:
    print("Start Testing...")
    con.test(name + ".txt")

execution_time = str(datetime.timedelta(seconds=time.time() - start_time))

print("Execution Time: ", execution_time)
