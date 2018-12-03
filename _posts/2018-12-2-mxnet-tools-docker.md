---
layout: post
published: true
title: MXNet tools in docker
---

How to convert [MXNet model to Apple CoreML](https://github.com/apache/incubator-mxnet/tree/master/tools/coreml):

```
docker run -v "$PWD":/data --rm -it dharmeshkakadia/mxnet-coreml-tools-docker python mxnet_coreml_converter.py 
```

For example, if you want to convert Squeeznet model to coreml, to use with iOS. 
Run the following from the a directory containing Squeeznet model files ([Params](http://data.mxnet.io/models/imagenet/squeezenet/squeezenet_v1.1-0000.params), [symbols](http://data.mxnet.io/models/imagenet/squeezenet/squeezenet_v1.1-symbol.json),[labels](http://data.mxnet.io/models/imagenet/synset.txt)) and will generaete `squeezenetv11.mlmodel` in the current directory.

```
docker run -v "$PWD":/data --rm -it dharmeshkakadia/mxnet-coreml-tools-docker python mxnet_coreml_converter.py --model-prefix='/data/squeezenet_v1.1' --epoch=0 --input-shape='{"data":"3,227,227"}' --mode=classifier --pre-processing-arguments='{"image_input_names":"data"}' --class-labels /data/synset.txt --output-file="/data/squeezenetv11.mlmodel"
```

The `Dockerfile` is located on [github](https://github.com/dharmeshkakadia/mxnet-coreml-tools-docker).