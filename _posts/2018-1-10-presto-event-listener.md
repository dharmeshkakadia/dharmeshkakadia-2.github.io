---
published: true
layout: post
title: Write a Presto query logging plugin
---
[Presto](https://prestodb.io/) is a fast distributed SQL query engine for big data. I wrote a more [introductory](http://dharmeshkakadia.github.io/presto-hdinsight/) and up and running post a while back.

Presto users frequently [[1](https://stackoverflow.com/questions/47286733/logging-all-presto-queries), [2](https://groups.google.com/forum/#!topic/presto-users/9jV7iOfdqeY), [3](https://groups.google.com/forum/#!topic/presto-users/zN2DFnzy5bs), [4](https://groups.google.com/forum/#!topic/presto-users/i1aG5LO40SY)] want the ability to log various details regarding queries and execution information from Presto. This is very useful for operationalizing presto in any organization. Logging query details allows a team to understand the usage of Presto, provide operational analytics and identify on performance bottlenecks. If you want to know how to achieve this, read on. You can also use this guide to learn how to implement any presto plugin. All the [code](https://github.com/dharmeshkakadia/presto-event-logger) used in this post is available. 

## Event Listeners

One of the best thing about Presto's design is clean abstractions. Event Listener is one such abstraction. Presto added Event Listener support some time back, similar to other engines. [Presto Event Listener](https://prestodb.io/docs/current/develop/event-listener.html) allows you to write custom functions that listens to events happening inside engine and react to it. Event listeners are invoked for following events in presto query workflow :

1. Query creation
2. Query completion
3. Split completion

Couple of caveats regarding Event Listeners in Presto:

* In a given presto cluster, you can only register a single event listener plugin.
* Each presto event listener is a presto plugin. So, it will behave like one - in terms of how is it registered and so on. 

So, to crate a query logging presto plugin, at a high level, we will,

1. Implement an `EventListener` and an `EventListenerFactory` interfaces from Presto. 

2. Make sure to package our classes and register the plugins so that Presto can find them. 

3. Deploy the plugin to Presto.

If these names dont make sense right now, don't worry. We will go through detailed step by step instructions below.

## Implementation

1. We will use [Maven](https://maven.apache.org/) for dependency management and packaging. Set it up and create an empty maven project.

2. Add Presto as dependency by adding the following into `project` section of the `pom.xml` file.

    ```xml
      <dependencies>
          <dependency>
              <groupId>com.facebook.presto</groupId>
              <artifactId>presto-spi</artifactId>
              <version>0.172</version>
              <scope>provided</scope>
          </dependency>
      </dependencies>
    ```  

    We will also use slf4j for logging the query details. Note that we used `logger` interface for logging the queries because it provides maximal flexibility on choosing where/how to store logs. So lets add that as a dependency as well
  
    ```xml
      <dependency>
        <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
            <version>1.7.16</version>
      </dependency>
    ```

3. Time to write code. We will start by creating [QueryFileLoggerEventListener](https://github.com/dharmeshkakadia/presto-event-logger/blob/master/src/main/java/QueryFileLoggerEventListener.java) class that implements Presto' [EventListener](https://github.com/prestodb/presto/blob/master/presto-spi/src/main/java/com/facebook/presto/spi/eventlistener/EventListener.java) interface. 

    ```java
    public class QueryFileLoggerEventListener implements EventListener{
    static final Logger logger = LoggerFactory.getLogger(QueryFileLoggerEventListener.class);

    public QueryFileLoggerEventListener(Map<String, String> config){}

    public void queryCompleted(QueryCompletedEvent queryCompletedEvent) {
      logger.info(queryCompletedEvent.getMetadata().getQueryId() + " : " +
        queryCompletedEvent.getMetadata().getQueryState() + " : " +
        queryCompletedEvent.getMetadata().getQuery() + " : " +
        queryCompletedEvent.getStatistics().getTotalRows() + " : " +
        queryCompletedEvent.getStatistics().getTotalBytes() + " : ");
      }
    }
    ```

    Here we are logging query details(`QueryId`, `State`, `Query`) and Statistics(`TotalRows`, `TotalBytes`) separating them via ` : ` in a single log line. Note that here for the space reason I am showing only few query details, event object contains a lot of other useful information. For example, you can use the `State` to determine if query failed or succeeded and log different details in each case. The code in the repo logs additional details.

    Also, note that we have only implemented `queryCompleted()` method from the EventListener interface. It provides `queryCreated()` and `splitCompleted()` methods for query creation and split completion event notifications.

4. Now lets create a [QueryFileLoggerEventListenerFactory](https://github.com/dharmeshkakadia/presto-event-logger/blob/master/src/main/java/QueryFileLoggerEventListenerFactory.java) class that implements Presto's [EventListenerFactory](https://github.com/prestodb/presto/blob/master/presto-spi/src/main/java/com/facebook/presto/spi/eventlistener/EventListenerFactory.java) interface.

    ```java
    public class QueryFileLoggerEventListenerFactory implements
      EventListenerFactory {
      public String getName() {
        return "event-logger";
      }

      public EventListener create(Map<String, String> config) {
        return new QueryFileLoggerEventListener(config);
      }
    }
    ```

    Here we are creating a minimal implementation of the factory method that is just invoking our listener. If you need to perform any additional initialization, you can add it here. Also, note that we are naming our logging listener `event-logger`, which we will use later when configuring it.

5. As noted previously, event listeners are registered as a plugin in Presto. So, lets create [QueryFileLoggerPlugin](https://github.com/dharmeshkakadia/presto-event-logger/blob/master/src/main/java/QueryFileLoggerPlugin.java) which implements Presto's Plugin

    ```java
    public class QueryFileLoggerPlugin implements Plugin {
      public Iterable<EventListenerFactory> getEventListenerFactories() {
        EventListenerFactory listenerFactory = new QueryFileLoggerEventListenerFactory();
        return ImmutableList.of(listenerFactory);
      }
    }
    ```

    Here we are again simply registering our factory as part of the plugin.

## Packaging

Now, that we have all the code, lets move to packaging it.
  
6. Presto uses [Service Provider Interfaces(SPI)](https://docs.oracle.com/javase/tutorial/sound/SPI-intro.html) to extend Presto. SPI is widely used in Java world. Presto uses [SPI](https://prestodb.io/docs/current/develop/spi-overview.html) to load [Connector](https://prestodb.io/docs/current/develop/connectors.html), [Functions](https://prestodb.io/docs/current/develop/functions.html), [Types](https://prestodb.io/docs/current/develop/types.html) and [System Access Control](https://prestodb.io/docs/current/develop/system-access-control.html). SPI are loaded via metadate files. We will create [`src/main/resources/META-INF/services/com.facebook.presto.spi.Plugin`](https://github.com/dharmeshkakadia/presto-event-logger/blob/master/src/main/resources/META-INF/services/com.facebook.presto.spi.Plugin) metadata file. The file should contain the class name for our plugin - `QueryFileLoggerPlugin`.

7. We will also add [`log4j.properties`](https://github.com/dharmeshkakadia/presto-event-logger/blob/master/src/main/resources/log4j.properties) file that specifies where to write our query logs. You should adopt this to your environment. 
  
8. Lets compile and package our code.
  
    ```shell
    mvn package
    ```

## Deployment

At this stage, we have our code ready to deploy to Presto. 

9. First we will have to tell Presto to load our listener. We will create event-listener configuration file `<path-to-presto>/etc/event-listener.properties`. This configuration file at-least should have `event-listener.name` property whose value should match the string returned by `EventListenerFactory.getName()` - in out case `event-logger`. The remaining properties will be passed as a map to `EventListenerFactory.create()` which can use for passing any additional information you want to your listener.

10. Copy our generated jar to the presto plugins directory.

    ```shell
    cp target/presto-event-logger*.jar <path-to-presto>/plugin/event-logger/
    ```
    
    You should also copy `slf4j-api-*.jar`, `slf4j-log4j12-*.jar`, `guava-*.jar`, `log4j-*.jar` or any additional dependencies that you have to the event-logger folder `<path-to-presto>/plugin/event-logger/`.

11. We are all set. Start the presto server

    ```shell
      <path-to-presto>/bin/launcher start  
    ```

    You should see the event listener registration in the Presto server logs. And you should also see your query logs as the queries are submitted to Presto.

That's it. We saw how to write a query logger plugin for presto. As noted above, [complete code](https://github.com/dharmeshkakadia/presto-event-logger) is available. Give it a try!