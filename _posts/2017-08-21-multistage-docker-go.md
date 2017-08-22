---
published: true
title: Multi stage docker build for go
---
Support for multistage docker build has landed in Docker earlier this year. Multi stage builds simplify the image building and the genereated images are much smaller in the size. The code/instructions are available at [go-multi-stage-docker](https://github.com/dharmeshkakadia/go-multi-stage-docker)

1. Here is our lovely go program that we want to run in the image:

  ```go
  package main

  import "fmt"

  func main() {
      fmt.Println("Hello Multistage Docker builds!")
  }

  ```

2. Here is the `Dockerfile` that you can use:

    ```Dockerfile
    # gobase layer
    FROM golang:alpine AS go-base
    ADD . /src
    RUN cd /src && go build -o hello

    # final layer
    FROM alpine
    COPY --from=go-base /src/hello /app/
    ENTRYPOINT /app/hello
    ```

    Here we create two layers:
     * go-base layer: Includes go runtime. We are mounting src directory in the image and compiling our go package(hello.go) and generating the output binary hello.
     * app layer: Extends the alpine image by copying our binary(/src/hello) from the go-base layer to /app/. It also defines entrypoint for the image as our binary(/app/hello)


3. Lets build our image and name it `go-multi-stage-docker` :
    ```
    $ docker build -f Dockerfile -t go-multi-stage-docker:latest .
    ```
  
  You can see the new image would be only few MBs in the size :

    ```
    $ docker image ls go-multi-stage-docker

    REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
    go-multi-stage-docker   latest              5f037e697b51        4 minutes ago       5.52MB
    ```
  
4. Lets run our app/image
	
    ```
    $ docker run --rm go-multi-stage-docker

    Hello Multistage Docker builds!
    ```
    
Thats it !
