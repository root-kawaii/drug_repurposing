from OpenKE import models
from OpenKE import config
import tensorflow as tf
import numpy as np
import os
os.environ['CUDA_VISIBLE_DEVICES']='0'

import tensorflow as tf

# Remove TF info and warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

relation_dimension = 10
entity_dimension = 200

con = config.Config()
con.set_in_path("../KnowledgeGraph/")
con.set_test_link_prediction(True)
#con.set_test_triple_classification(True)
con.set_work_threads(8)
con.set_rel_dimension(relation_dimension)
con.set_ent_dimension(entity_dimension)
con.set_import_files("../Result_Embedding/TransE_10_0.001_200_1_1_0_100.model.vec.tf")
con.init()
con.set_model(models.TransE)
con.test("edo.txt")

a = con.predict_tail_entity(21554, 64, 100000)

#print(np.where(a == 15142))

#con.predict_triple(21554, 15142, 64)

#con.import_variables("../DrugRepurposing/Result_Embedding/")

# #True: Input test files from the same folder.
# # con.set_in_path("../KnowledgeGraph/")
# # con.set_test_link_prediction(True)
# #con.set_test_triple_classification(True)
# con.set_test_link_prediction(True)
#
# con.set_nbatches(200)
# con.set_alpha(0.001)
# con.set_margin(1.0)
# con.set_bern(0)
# con.set_dimension(150)
# con.set_ent_neg_rate(1)
# con.set_rel_neg_rate(0)
# con.set_opt_method("SGD")
#
# con.set_import_files("../Result_Embedding/model.vec.tf")
# con.set_in_path("../KnowledgeGraph/")
#
# # # Models will be exported via tf.Saver() automatically.
# # con.set_export_files("../Result_Embedding/model.vec.tf", 0)
# #
# # # Model parameters will be exported to json files automatically.
# # con.set_out_files("../Result_Embedding/embedding.vec.json")
#
# # Initialize experimental settings.
# con.init()
#
# # Set the knowledge embedding model
# con.set_model(models.TransE)
#
# # To test models after training needs "set_test_flag(True)".
# con.test()
# # con.predict_head_entity(152, 9, 10)
# #a = con.predict_tail_entity(20625, 64, 10)
# #print(type(a))
# # con.predict_relation(151, 152, 5)
# #con.predict_triple(151, 152, 9)
# # con.predict_triple(151, 152, 8)
#
#
# # # Magic
# #
# # kg_path = "../KnowledgeGraph/"
# # relation_dictionary = {}
# # with open(kg_path + "relation2id.txt", "r") as file:
# #     file.readline()
# #     for line in file:
# #         line_list = line.strip().split("\t")
# #         name = line_list[0]
# #         id_rel = line_list[1]
# #         relation_dictionary[name] = id_rel
# #
# # print(relation_dictionary["TREAT"])

