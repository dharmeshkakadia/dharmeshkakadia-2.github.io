---
layout: page
# title: Reading
permalink: /reading/
published: true
---

<!-- Here is how I am reading on Pocket.

{% include pocket_per_day.html %}

{% include pocket_week.html %} -->

### Here are the books I have [read](https://www.goodreads.com/author/show/14159157.Dharmesh_Kakadia):

<main class="shelf">
  {% for book in site.data.books  %}
  <article class="book">
    <figure class="book-cover">
      <a href="https://www.goodreads.com/book/isbn/{{ book.Book_Id }}">
        <img src="/images/books/{{ book.Book_Id }}.jpeg" alt="{{ book.Title }}" style="border:1px solid black; vertical-align: bottom;">
        <div class="book-info">
          <p class="book-title" style="">{{ book.Title }}</p>
          <p class="book-author">{{ book.Author }}</p>
        </div>
      </a>
    </figure>
  </article>
  {% endfor %}
</main>