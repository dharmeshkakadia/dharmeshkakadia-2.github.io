---
published: false
---
## Multi stage docker build for go
Support for multistage docker build has landed in Docker earlier this year. One of the prime benefit of multi stage docker builds are the size of the generated images.

Here is our lovely go program that we want to run in the image:

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello Multistage Docker builds!")
}

```

