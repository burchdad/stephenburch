---
layout: default
title: Blog
permalink: /blog/
---

<section class="blog">
    <h2>Blog</h2>
    <ul>
        {% for post in site.posts %}
            <li>
                <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
                <p><small>{{ post.date | date: "%B %d, %Y" }}</small></p>
                <p>{{ post.excerpt }}</p>
            </li>
        {% endfor %}
    </ul>
</section>
