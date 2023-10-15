---
date: 15 Oct, 2023
tags: micropython, embedded, esp8266
category: engineering
---

# Cableless Development with Micropython Server

Ever tired of having to connect your microcontroller to your laptop with a cable? Wifi-able chips
and remote servers come to the rescue.

I encountered this problem recently when I was building a robot car to prepare for the
[Scioly Robot Tour Event](https://www.soinc.org/). This is why I hand-wrote a tiny http server based
on [Microdot](https://github.com/miguelgrinberg/microdot) to deal with this situation.

This server is capable of displaying the files stored on your microcontroller as well as updating them
through an http POST request.

The following is the entire Python script for the server.

```{code-block} python
:linenos:
:caption: server.py

from microdot import Microdot
from tarfile import TarFile
from pathlib import Path
from network import WLAN

import tarfile
import network
import time
import os
import io

server = Microdot()

DIR_HTML = """\
<html>
    <head>
        <title>{dir}</title>
    </head>
    <body>
        <h1>{dir}</h1>
        <ul>
            {files}
        </ul>
    </body>
<html>
"""

DIR_ELEMENT = """\
<li>
    <a href="{url}">{text}</a>
</li>
"""

HOST_CONFIG = {
    "essid": "<your-ssid>",
    "password": "<your-password>"
}


@server.post("/update")
def update_program(request):
    tar = TarFile(fileobj=io.BytesIO(request.body))
    try:
        for file in tar:
            if file.type == tarfile.DIRTYPE:
                Path(file.name).mkdir(parents=True, exist_ok=True)
            else:
                contents = tar.extractfile(file)
                Path(file.name).write_bytes(contents.read())
    except OSError as e:
        return {
            "status": "error",
            "details": str(e),
        }

    return {"status": "success"}


def _format_html(path):
    return DIR_HTML.format(
        dir=path,
        files="\n".join(
            DIR_ELEMENT.format(
                url=f"/files{(path / file).resolve()}",
                text=file,
            )
            for file in os.listdir(path.resolve())
        ),
    ), {"Content-Type": "text/html"}


@server.get("/files")
def display_file_root(request):
    return _format_html(Path("/"))


@server.get("/files/<path:path>")
def display_file(request, path):
    path = Path(path)
    if not path.exists():
        return str(path), 404
    if path.is_file():
        return path.read_text(), {"Content-Type": "text/plain"}

    # a directory
    return _format_html(path)


@server.get("/shutdown")
def shutdown(request):
    request.app.shutdown()
    return {"status": "success"}


def setup():
    ap = WLAN(network.AP_IF)
    ap.active(True)
    ap.config(**HOST_CONFIG)

    while not ap.active():
        time.sleep_ms(100)


def run():
    server.run()
```

To run this server, first install the necessary packages with [`mip`](https://docs.micropython.org/en/latest/reference/packages.html):

```python
import mip
mip.install("tarfile")
mip.install("pathlib")
mip.install("github:miguelgrinberg/microdot/src/microdot.py")
```

```{note}
You may need to compile `microdot.py` with [`mpy-cross`](https://github.com/micropython/micropython/tree/master/mpy-cross) to avoid `MemoryError`s.
```

Then simply import the server and run it!

```python
import server
server.setup()
server.run()  # This will never return unless shutdown is requested
```

After running it, connect your laptop to the microcontroller via WiFi and go to
http://192.168.4.1:5000/files (or whichever IP your server is running on) and you should see your files!

To update the files via the server, archive your code with `tar` and send an http POST request to
http://192.168.4.1:5000/update. With `tar` and [`httpx`](https://www.python-httpx.org/), it looks like this:

```bash
tar -cf app.tar ./app
```

followed by

```python
import httpx
httpx.post(
    f"http://192.168.4.1:5000/update",
    content=b"<tar file in bytes>",
)
```

Have fun developing cableless!

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
