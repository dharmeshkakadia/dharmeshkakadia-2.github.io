---
published: false
layout: post
title: How to write a Presto Event Listener
---

Presto added Event Listener support some time back.
[Presto Event Listener](https://prestodb.io/docs/current/develop/event-listener.html) allows you to write a custom event listeners.

Event lisnters are invoked for following events in presto query workflow :
1. Query creation
2. Query completion
3. Split completion

In a given presto cluster, you can only register a single event listener plugin.

Note that each presto event listener is a presto plugin. So, it will behave like one - in terms of how is it registered and so on.

To implement an event listener you have to implement X
You will also have to create a configuration file etc/event-listener.properties 

The configuration file atleast should have ``event-listener.name`` property whose value should match the string returned by ``EventListenerFactory.getName()``. The remaining properties will be passed as a map to ``EventListenerFactory.create()``.

It opens up nice use case in terms of operations and support. 

Step by step instructions

1. Write a event listener

  1. Set up an empty maven project

  2. Add presto dependency

  3. Add event lister class, factory and plugin

  4. Add SPI plugin in metadate 

  5. Add log4j Properties

  6. compile and package the jar

7. Copy the jar as part of presto plugins

8. Start the presto server


What info is available inside the events.

https://github.com/dharmeshkakadia/presto-event-logger

