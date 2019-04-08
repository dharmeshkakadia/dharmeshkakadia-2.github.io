---
layout: post
published: false
title: Tensorflow Estimators
---

https://www.tensorflow.org/guide/estimators
Estimators represents a complete model. The Estimator is a high level API that provides methods to train the model, to judge the model's accuracy, and to generate predictions.
You can either use premade Estimators or create your own

https://www.tensorflow.org/tutorials/estimators/linear
THe whitepaper has more details https://arxiv.org/abs/1708.02637


Estimators provide the following benefits:

You can run Estimator-based models on a local host or on a distributed multi-server environment without changing your model. Furthermore, you can run Estimator-based models on CPUs, GPUs, or TPUs without recording your model.
Estimators simplify sharing implementations between model developers.
You can develop a state of the art model with high-level intuitive code. In short, it is generally much easier to create models with Estimators than with the low-level TensorFlow APIs.
Estimators are themselves built on tf.keras.layers, which simplifies customization.
Estimators build the graph for you.
Estimators provide a safe distributed training loop that controls how and when to:

build the graph
initialize variables
load data
handle exceptions
create checkpoint files and recover from failures
save summaries for TensorBoard

When writing an application with Estimators, you must separate the data input pipeline from the model. This separation simplifies experiments with different data sets.


