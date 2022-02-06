from OpenKE import models

list_parameters = ["model", "epoch", "alpha", "relation_dimension", "entity_dimension",
                   "margin", "ent_neg_rate", "rel_neg_rate", "number_batch", "optimization_method"]


def produce_name(delimiter="_", **kwargs):
    result = ""
    for param in list_parameters:
        if param == "model":
            result += str(kwargs[param].__name__) + delimiter
        else:
            result += str(kwargs[param]) + delimiter

    result = result[:-1]
    return result


def get_parameters(name, delimiter="_"):
    result = {}
    splitted_name = name.split(delimiter)
    for i in range(len(list_parameters)):
        result[list_parameters[i]] = splitted_name[i]
    return result


def get_model(model_name):
    if model_name == "TransE":
        return models.TransE
    elif model_name == "TransD":
        return models.TransD
    elif model_name == "TransH":
        return models.TransH
    elif model_name == "TransR":
        return models.TransR
    elif model_name == "HolE":
        return models.HolE
    elif model_name == "RESCAL":
        return models.RESCAL
    elif model_name == "Analogy":
        return models.Analogy
    elif model_name == "ComplEx":
        return models.ComplEx
    elif model_name == "DistMult":
        return models.DistMult
