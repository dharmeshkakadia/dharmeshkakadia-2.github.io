---
published: false
---
## How to write a Presto Event Listener

Presto added Event Listener support some time back.

It opens up nice use case in terms of operations and support. 

Step by step instructions

1. Write a event listener

  1. Set up an empty maven project

  2. Add presot dependency

  3. Add event lister class, factory and plugin

  4. Add SPI plugin in metadate 

  5. Add log4j Properties

  6. compile and package the jar

7. Copy the jar as part of presto

8. Start the presto server


What info is available inside the events.

https://github.com/dharmeshkakadia/presto-event-logger

