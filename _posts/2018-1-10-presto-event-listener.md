---
published: false
layout: post
title: How to write a Presto Event Listener
---
Presto is [a fast distributed SQL query engine for big data](http://dharmeshkakadia.github.io/presto-hdinsight/).
Presto added Event Listener support some time back.
[Presto Event Listener](https://prestodb.io/docs/current/develop/event-listener.html) allows you to write a custom event listeners.

Event listeners are invoked for following events in presto query workflow :
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

Write a event listener

  1. Set up an empty maven project

  ```shell
  git clone https://github.com/dharmeshkakadia/presto-event-logger && cd presto-event-logger
  ```

  This is how the project will look like
  ```shell
  tree
  ```

  2. Add presto dependency by adding the following into ``project`` section of the ``pom.xml`` file.

  ```xml
    <dependencies>
        <dependency>
            <groupId>com.facebook.presto</groupId>
            <artifactId>presto-spi</artifactId>
            <version>0.172<</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>
  ```  

3. Add event lister class, factory and plugin

4. Add SPI plugin in metadate file ``src/main/resources/META-INF/services/com.facebook.presto.spi.Plugin``. The file should container ``QueryFileLoggerPlugin``.


5. Add log4j Properties
  ```shell
  vim src/main/resources/log4j.properties
  ```

6. compile and package the jar
  ```shell
  mvn package
  ```

7. Copy the jar to the presto plugins directory.
  ```shell
  cp target/presto-event-logger*.jar <path-to-presto>/plugin/event-logger/
  ```
    
  You should also copy ``slf4j-api-*.jar``, ``slf4j-log4j12-*.jar``, ``guava-*.jar``, ``log4j-*.jar`` to the event-logger folder ``<path-to-presto>/plugin/event-logger/``. 

8. Start the presto server
  ```shell
    <path-to-presto>/bin/launcher start  
  ```


In the above example we have only used ``queryCompleted()`` [link] method from the [EventListener](link) interface. It provides following methods for different event notifications.

What info is available inside the events.

Also, note that we used logger interface for logging the queries because it provides maximal flexibility 

At high level, I am bit skeptic, and the finding data that supports authors arguments, is always possible.

https://github.com/dharmeshkakadia/presto-event-logger

