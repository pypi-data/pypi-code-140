#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
Function for model naming
"""

import tensorflow as tf
from cnn2snn.cnn2snn_objects import cnn2snn_objects


def _split_item(full_name):
    """Splits name and number from a string that ends in digits.

    Args:
        full_name (str): the string to split

    Returns:
        tuple: the name and the number as strings
    """
    num = ""
    i = len(full_name) - 1
    while i >= 0 and full_name[i].isdigit():
        num = full_name[i] + num
        i -= 1
    name = full_name[:len(full_name) - len(num)]
    return name, num


def _old_name_2_new_name(old_name):
    """Convert a layer name from old naming convention to new one.

    Args:
        old_name (str): the old name

    Returns:
        str: the converted name
    """
    # suppress numberting
    if old_name.startswith("input_"):
        return "input"
    if old_name.startswith("rescaling_"):
        return "rescaling"
    if old_name.startswith("flatten_"):
        return "flatten"

    # construct the new name
    new_name = ""
    splitted_name = old_name.split("_")

    # post fixed first
    postfix = ""
    if splitted_name[-1] in ("relu", "maxpool", "BN"):
        postfix = "/" + splitted_name[-1]
        del splitted_name[-1]
    elif len(splitted_name) > 2 and splitted_name[-1] == "avg" and splitted_name[-2] == "global":
        postfix = "/global_avg"
        splitted_name = splitted_name[:-2]

    for item in splitted_name:
        # splits the name and the layer number if there are together
        assert len(item) > 0
        name, num = _split_item(item)

        if len(name) > 0 and len(num) > 0:
            new_name += name + "_" + num + "/"
        elif len(name) == 0:
            new_name += num + "/"
        else:
            new_name += name + "_"

    # remove last separator ("/" or "_")
    new_name = new_name[:-1]
    new_name += postfix

    # sepcifics conversion for modelnet40 model
    m40_subs = {}
    m40_subs["re_lu"] = "block_1/conv_1/relu_1"
    m40_subs["re_lu_1"] = "block_1/conv_2/relu_1"
    m40_subs["re_lu_2"] = "block_2/conv_1/relu_1"
    m40_subs["re_lu_3"] = "block_2/conv_2/relu_1"
    m40_subs["re_lu_4"] = "block_3/conv_1/relu_1"
    m40_subs["re_lu_5"] = "block_3/conv_2/relu_1"
    m40_subs["re_lu_6"] = "block_4/conv_1/relu_1"
    if new_name in m40_subs.keys():
        new_name = m40_subs[old_name]
    # fix typo
    elif new_name.startswith("bloc_1/"):
        new_name = "block_1/" + new_name[7:]

    return new_name


def rename_model_layers(model, custom_objects=None, renaming_function=_old_name_2_new_name):
    """Renames the layers of a model while keeping the pre-trained weights.

    Args:
        model (tf.keras model): the model to rename layers
        custom_objects (dict): if your model consists of custom layers you should, add them passed
            as a dictionary. For more information read the following:
            https://keras.io/guides/serialization_and_saving/#custom-objects
        renaming_function (function): a function that returns a new name from an old one.
            `function(old_name: str)-> str`.
    Returns:
        tf.keras model: a model having same weights as the input model.
    """

    if custom_objects is None:
        custom_objects = {}
    all_custom_objects = {**custom_objects, **cnn2snn_objects}

    config = model.get_config()
    old_to_new = {}
    new_to_old = {}

    for layer in config['layers']:
        old_name = layer['name']
        new_name = renaming_function(old_name)
        old_to_new[layer['name']], new_to_old[new_name] = new_name, layer['name']
        layer['name'] = new_name
        layer['config']['name'] = new_name

        if len(layer['inbound_nodes']) > 0:
            for in_node in layer['inbound_nodes'][0]:
                in_node[0] = old_to_new[in_node[0]]

    if 'input_layers' in config.keys():
        for input_layer in config['input_layers']:
            input_layer[0] = old_to_new[input_layer[0]]

    if 'output_layers' in config.keys():
        for output_layer in config['output_layers']:
            output_layer[0] = old_to_new[output_layer[0]]

    new_model = tf.keras.Model().from_config(config, all_custom_objects)

    new_model.set_weights(model.get_weights())

    return new_model
