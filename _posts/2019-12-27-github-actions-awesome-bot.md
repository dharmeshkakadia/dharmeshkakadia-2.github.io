---
layout: post
published: true
title: Verifying links with Github actions & Awesome Bot
---

Recently I started using [github action](https://github.com/features/actions) to automate link checking in all of [my awesome repos](https://github.com/dharmeshkakadia?utf8=%E2%9C%93&tab=repositories&q=awesome&type=&language=). I have been using [awesome_bot](https://github.com/dkhamsing/awesome_bot) to validate links and checks for duplicates, with [travis](https://travis-ci.org/) since past 2+ years. I decided to give github actions try with this very simple automation. Github action is very rich and can automate a lot of chores for developers. There are number of existing actions available in the [github market place](https://github.com/marketplace?type=actions). However, I couldn't find one that allows me to verify links in markdown. So lets build one from [scratch](https://github.com/dharmeshkakadia/awesome-mesos/pull/45)!

Here is my github action config : 

```
name: CI

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v1
    - uses: docker://dkhamsing/awesome_bot:latest
      with:
        args: --allow-redirect /github/workspace/README.md
```

You can put this under `.github/workflows/main.yaml` in your repo and voila!

Now let's go through the file to understand whats going on here. `name` is just a display name used. `on` specifies when this workflow runs. There are number of [options available](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows), but here we just need to run it on every `push`. We can filter which branches this triggers work etc. However we don't need them for this. Just know that [Github actions syntax](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions) is very flexible.

`jobs` is where the meat of the workflow is. Here you can specify what you actually want to do as part of this workflow. In our workflow we only have job with `job_id` as `build`. If we specify more jobs it by default runs in parallel, but we can create dependency chains using `jobs.<job_id>.needs` tag. We are specifying that the job should run on `ubuntu-latest` agent. We need to use ubuntu agent when running a docker image with github action. 

Now a job consists of a multiple tasks called `steps`. Here we are using two steps. First a github provided action called `actions/checkout@v1` to checkout the code. Second we are specifying a docker action with `dkhamsing/awesome_bot:latest` docker image. This is the docker image recommended by [awesome_bot repo](https://github.com/dkhamsing/awesome_bot#docker-examples). We are specifying here that awesome_bot should respect redirects and specifying the file path for our markdown file. Note that the checkout code is mapped as `/github/workspace/` while running with docker. This bit of information wasn't easy to find out and took few iteration to get right. That's it! You are all set now. All the PRs will now automatically run awesome bot to check the links and validation results will be visible on the PR page itself! You can look at [some pull requests](https://github.com/dharmeshkakadia/awesome-mesos/pull/46) if you want example - click on green checkmark on right and then on `Details` next to `CI/build (push)` and you will see the full logs of validation under `actions` tab in the repository.

![Github actions logs]({{site.baseurl}}/images/github-actions-logs.png)

Happy hacking and happy holidays everyone !
