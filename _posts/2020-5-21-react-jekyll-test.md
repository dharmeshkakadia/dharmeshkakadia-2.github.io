---
layout: post
published: true
title: Using react components with Jekyll on Github Pages
tags: [React, Jekyll, github-pages]
# image: /images/spark-arch.png
---
Why? because we can
  <h2>Add React in One Minute</h2>
  <p>This page demonstrates using React with no build tooling.</p>
  <p>React is loaded as a script tag.</p>

  <!-- We will put our React component inside this div. -->
  <div id="like_button_container"></div>

  <!-- Load React. -->
  {% include react.html %}
  <!-- Load our React component. -->
  <script src="{{ site.baseurl }}/components/like_button.js"></script>

Thats it !
