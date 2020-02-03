---
layout: post
published: false
title: Internals of Spark Parser
---

Spark is a widely used analytics and machine learning engine, which you have probably heard of. You can use Spark with various languages - Scala, Java, Python - to perform a wide variety of tasks - streaming, ETL, SQL, ML or graph computations. Spark SQL/dataframe is one of the most popular ways to interact with Spark. Spark SQL provides SQL syntax and SQL like API to build complex computation graphs. Spark SQL relies on a common compiler framework to translate the high level SQL code into executable low level code. Spark Catalyst is the name of that compiler framework. 

### Catalyst Architecture

Following image describes various steps and components of Spark Catalyst. The image is taken from [databricks](https://databricks.com/glossary/catalyst-optimizer)
![spark-arch.png]({{site.baseurl}}/images/spark-arch.png)

Like any compiler [may be cite] Spark Catalyst compiler has a various modules for different phases of compilation process.

TODO: explain briefly each phases.
TODO: show it contains tree/operator manipulation primitives 

In this post we will focus more on parser part of the Catalyst.

### Need for a formally defined grammar and parser

Grammar+Parser helps in answering the following question: Is given statement complaint to the rules of the language. 
Some ``select * from sample`` is valid Spark statement or not?


### Why we need to understand parser 

* Will/Why is the given statement giving error on parsing?
* Is this a keyword in Spark or not? 
* Add new feature (say merge statement support)
* Build new tools, say our own editor for Spark..
* Generating automated tests from the grammer

### ANTLR

* ANother Tool for Language Recognition. 
* Parser generator for reading, processing, executing, or translating structured text.
* ANTLR generates a parser that can build and walk parse trees.
* Toolkit for building languages
* Used widely by many languages (Groovy, Cassandra, Hive, …)
* Spark parser first tries to parse it using SLL mode (Strong LL), which is faster. If that fails, it will try to parse it as LL.


### ANTLR grammar 

* Spark grammar is LL. 
* LL stands for Left to right parsing, deriving leftmost derivation.


* A grammar G = ( N, T, P, S ) is said to be strong LL(k) for some fixed natural number k if for all nonterminals A, and for any two distinct A-productions in the grammar. 
* The strong LL(k) grammars are a subset of the LL(k) grammars that can be parsed without knowledge of the left-context of the parse. That is, each parsing decision is based only on the next k tokens of the input for the current nonterminal that is being expanded. Or in other words, parsers that ignore the parser call stack for prediction are called Strong LL (SLL) parsers.


* **Spark parser first tries to parse it using SLL mode (Strong LL), which is faster. If that fails, it will try to parse it as LL.**

### ANTLR operators

```
| alternatives
. any character
? repeated zero or one time
+ repeated one or more times
* repeasted zero or more times
```

### Simple ANTLR end to end example

A very simple codebase that implements the following [grammer](https://github.com/dharmeshkakadia/hello-antlr/blob/master/src/main/antlr4/Hello.g4):

```antlr-java
grammar Hello;
msg   : 'Hello' ID;
ID  : [a-z]+ ;
WS  : [ \t\r\n]+ -> skip ;
```

Then we have to implement Visiter interface to decide what to do when we encounter/parse/traverse a node in the grammar

```java
public class HelloVister extends HelloBaseListener {
public void enterMsg(HelloParser.MsgContext ctx){
	System.out.println("Entering Msg : " + ctx.ID().getText());
}
	public void exitMsg(HelloParser.MsgContext ctx){
		System.out.println("Exiting Msg");
	}
}
```

Now we have to initilize the lexer, parser etc.

```java
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

public class Hello {
	public static void main(String[] args) {
		HelloLexer lexer = new HelloLexer(new ANTLRInputStream("Hello world"));
		HelloParser parser = new HelloParser(new CommonTokenStream(lexer));
		ParseTreeWalker visiter = new ParseTreeWalker();
		visiter.walk(new HelloVister(),parser.msg());
	}
}

```


This has a maven antlr integration, which takes care of generating the code for the grammar as well. To compile

```
mvn compile
```

To run it, use

```
mvn exec:java -q
```

which would print
```
Entering Msg : world
Exiting Msg

```

P.S. This post is made from the the notebook that I used at Microsoft team for our internal [presentation](https://github.com/dharmeshkakadia/spark-internals), but was not published here on blog. 