---
date: 6 Aug, 2023
tags: database, sqlite, nlp
category: machine-learning
---

# Sentiment analysis with a SQLite database (...and TF-IDF)

Today I'm just starting Chapter 8: Sentiment Analysis in [the book](https://github.com/rasbt/machine-learning-book).
But this time I'm not just busy scribbling down notes or copying code verbatim into my Python REPL.
I decided to experiment with SQLite databases! (as you can probably infer from the title) Hopefully, I will
be able to practice both my ML and my DB skills 😅.

Consider this piece of code from the book, which is used to extract data from the IMDb dataset:

```python
basepath = 'aclImdb'

labels = {'pos': 1, 'neg': 0}
pbar = pyprind.ProgBar(50000, stream=sys.stdout)
df = pd.DataFrame()
for s in ('test', 'train'):
    for l in ('pos', 'neg'):
        path = os.path.join(basepath, s, l)
        for file in sorted(os.listdir(path)):
            with open(os.path.join(path, file), 
                      'r', encoding='utf-8') as infile:
                txt = infile.read()
            df = df.append([[txt, labels[l]]], 
                           ignore_index=True)
            pbar.update()
df.columns = ['review', 'sentiment']
```

(pos and neg refer to sentiment labels, all text files under pos are positive reviews and vice versa)

Instead of directly storing the data in a Pandas DataFrame, I attempted to store it in a SQLite Database
(by using the `sqlite3` package in the stdlib):

```{code-block} python
:linenos:

import sqlite3
from pathlib import Path

con = sqlite3.connect("IMDb.sqlite3")
con.execute("""
CREATE TABLE IF NOT EXISTS IMDb (
    id INTEGER PRIMARY KEY,
    review TEXT,
    sentiment INTEGER
)
""")

def get_count():
    return con.execute("SELECT COUNT(*) FROM IMDb").fetchone()[0]

if get_count() == 0:
    def reviews():
        for file in Path("aclImdb").glob("**/pos/*.txt"):
            with open(file, encoding="utf-8") as f:
                yield (f.read(), 1)
                
        for file in Path("aclImdb").glob("**/neg/*.txt"):
            with open(file, encoding="utf-8") as f:
                yield (f.read(), 0)
            
    cur = con.cursor()
    with con:
        cur.executemany(
            "INSERT INTO IMDb (review, sentiment) VALUES (?, ?)",
            reviews()
        )
        
    print(get_count())
```

First I created a connection with `sqlite3.connect()`. Then I created the table and inserted the
reviews into the table with basic CRUD operations.

```{note}
Highlights in the code above:

1. `CREATE TABLE IF NOT EXISTS`: only create the table if it does not exist
2. `reviews()` is a generator function (`yield`), so that I can use it in combination with `con.executemany()`
3. `with con`: Connection objects as context managers (auto `COMMIT` or `ROLLBACK`)
4. `VALUES (?, ?)`: SQL interpolation, prevents SQL injection
```

And finally, I need to read the reviews into a DataFrame, so as to preprocess the data. This time I chose [polars](https://www.pola.rs). Polars provides a function that utilizes [connectorx](https://sfu-db.github.io/connector-x/intro.html)
to load data from a variety of SQL databases. For me, I only need to provide the SQL `SELECT` statement and the connection url:

```python
import polars as pl
df = pl.read_database(
    "SELECT review, sentiment FROM IMDb",
    "sqlite://IMDb.sqlite3",
)
```

That's it! I succeeded in storing and retrieving data from a SQLite database.

Now it's time for some less hands-on stuff.

## TF-IDF

I've always heard people discussing TF-IDF, but not until today did I truly understand what it refers to
and why it's useful in NLP.

TF-IDF, which stands for term frequency-inverse document frequency, is used for highighting important words (but not common ones such as "is" or "a") in a document. It is defined as follows:

$$
\mathrm{tfidf}(t, d) = \mathrm{tf}(t, d)\cdot\mathrm{idf}(t, d)
$$

where $t$ is the term and $d$ is the document.

$\mathrm{tf}(t, d)$, of course is the number of occurances of a term in a document. $\mathrm{idf}(t, d)$, on the other hand is more complicated.

It's defined as:

$$
\mathrm{idf}(t, d) = \log\frac{n_d}{1 + \mathrm{df}(t)}
$$

where $n_d$ is the total number of documents and $\mathrm{df}(d, t)$ refers to the document frequency (how many documents contain the term $t$).

However, in scikit-learn, it is instead defined as:

$$
\mathrm{idf}(t, d) = \log\frac{1 + n_d}{1 + \mathrm{df}(t)}
$$

(which helps to prevent the singularity of $\log x$ at $x = 0$)

This way, when words such as "is" or "a" appear in every document, $\mathrm{df}(d,t)$ will be very large, and thus
$\mathrm{tfidf}(t, d)$ will be small.

That's all I have to share today.
