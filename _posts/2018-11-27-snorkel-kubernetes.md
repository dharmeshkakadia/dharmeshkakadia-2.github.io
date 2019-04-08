---
layout: post
published: false
title: How to run Snorkel on Kubernetes 
---

kubectl run -it snorkel-test --image vochicong/snorkel --port=8888

kubectl port-forward deploy/snorkel-test 8888:8888