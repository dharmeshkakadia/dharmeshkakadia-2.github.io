---
published: true
---
I wanted to give Go’s new dependency management system — [dep](https://github.com/golang/dep) - a try. I searched for a minimal example and did not find one. So here it is. The code/instructions are also located at [go-dep-example](https://github.com/dharmeshkakadia/go-dep-example)

0. Lets install dep. On mac, you can do the following:

	`brew install dep`

1. `dep init` This will generate following tree

    ```
        ├── Gopkg.lock
        ├── Gopkg.toml
        ├── README.md
        └── vendor
    ```

2. Now import the new package in the code. We will import [github.com/franela/goreq](github.com/franela/goreq). You will see your IDE complaining about not being able to find the package, since its not yet installed. We will do that next. You can confirm this by running `dep status`

3. Run dep ensure If you run `dep status` now it will confirm the package is installed. Also, the vendor directory now will have the following files from the package:
    ```
    vendor
        └── github.com
            └── franela
                └── goreq
                    ├── LICENSE
                    ├── Makefile
                    ├── README.md
                    ├── goreq.go
                    ├── goreq_test.go
                    └── tags.govendor
    ```

You are ready, go change the world !

P.S. This post is also published on [medium](https://medium.com/@dharmesh.kakadia/minimal-go-dep-example-54fc862615c4).
