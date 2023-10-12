---
date: 11 Oct, 2023
tags: object-detection, dataset
category: machine-learning
---

# Numbered Musical Notation Dataset -- Component Extraction 1

How to detect objects (extract components)? This is a crucial problem when I'm trying to extract
musical notation from typesetted images of numbered musical notation sheet music.

My first attempt:

![extracted components with opencv](../images/nmn-comp-ext/image.png)

As the sheet music is typesetted, it is relatively easy to use opencv to extract components purely by
analyzing connected components. However, this is less ideal when the image resolution is relatively low.

I'm planning to try RCNNs (a deep learning model for object detection) as an alternative solution.

<script src="https://giscus.app/client.js"
        data-repo="acciochris/acciochris.github.io"
        data-repo-id="R_kgDOKDyTVg"
        data-category="Announcements"
        data-category-id="DIC_kwDOKDyTVs4CYZPy"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
