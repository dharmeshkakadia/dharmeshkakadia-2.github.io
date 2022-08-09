---
layout: post
published: true
title: ML models - Where to serve?
tags: [machine-learning, deployment, engineering]
---

Offline:
TODO: Add Offline job Diagram
Precompute and serve via storage - database, NoSQL, blob,.. depending on the use case.

Client side:
TODO: Add Client side Diagram
Embedding model in the client is fairly common practice, especially as the framework like Tensorflow lite[] and SwiftML[?]and others have made is easier to integrate ML models in the client. There has been a lot of progress also in terms of the models themselves - and model compression and so on that makes this method very attractive.


Pros:
* No compute to maintain
* Privacy

Cons:
* Hard to control the upgrade cycle.


Server side:
TODO: Add Server side Service Diagram

Pros:
* 

Cons:

