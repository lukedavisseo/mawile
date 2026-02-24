# mawile (Meaningful Anchor \[Tags\] With Internal Links + Embeddings)

<a href="https://pokemondb.net/pokedex/mawile"><img src="https://img.pokemondb.net/sprites/emerald/back-shiny/mawile.png" alt="Mawile" width="64" height="64" align="right" style="image-rendering:pixelated;"></a>

> mawile is a [marimo app](https://marimo.app/) that recommends pages for internal linking based on cosine similarity between embeddings.

## Table of Contents
 - [Demo](#demo)
 - [Example use cases](#example-use-cases)
 - [Development](#development)
 - [Inspiration](#inspiration)
 - [License](#license)

# Demo

Coming soon...

# Example use cases

If you're looking to link from semantically similar pages to a target page that don't necessarily include exact match anchor text. Context is king!

# Development

- mawile was created by me.
  - I used Gemini for the bulk of the `filtered_df` function which maps the cosine similiarity score to each row of data
- Mawile, the Deceiver Pokémon, is the property of [Nintendo](https://www.nintendo.com/), [Game Freak](https://www.gamefreak.co.jp/), and [Creatures Inc](https://www.creatures.co.jp/).
- The cosine similarity function came from [Earthly](https://earthly.dev/blog/cosine_similarity_text_embeddings/)

## Inspiration

There are tons of ways to improve internal linking for a site but I've loved using embeddings for textual tasks so I thought why not use it here? The name came from 10 minutes of finding a Pokémon name that featured the letters **i** (for internal), **l** (for links/linking), and **e** (for embeddings) and creating a backronym out of the result. Mawile was the winner.

# License

mawile is released under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
