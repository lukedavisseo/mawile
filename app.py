# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy==1.26.4",
#     "polars",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(
    width="medium",
    app_title="mawile (Meaningful Anchor [Tags] With Internal Links + Embeddings)",
)


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import numpy as np

    return mo, np, pl


@app.cell
def _(np):
    # via https://earthly.dev/blog/cosine_similarity_text_embeddings/
    def cosine_similarity(vector_a, vector_b) -> np.float64:
        dot_product = np.dot(vector_a, vector_b)
        magnitude_a = np.linalg.norm(vector_a)
        magnitude_b = np.linalg.norm(vector_b)
        return dot_product / (magnitude_a * magnitude_b)


    return (cosine_similarity,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(f"""
    <h1>mawile
        <span style="height:32px;vertical-align: text-top;"><img src="https://camo.githubusercontent.com/3196d67bada8c480b50d9acb20145418be00a3c8a7294ae8266e135a1cb771b5/68747470733a2f2f696d672e706f6b656d6f6e64622e6e65742f737072697465732f656d6572616c642f6261636b2d7368696e792f6d6177696c652e706e67" width="32" height="32" style="display:inline;margin:0;padding:0" /></span>
    </h1>

    ### mawile is a marimo app that recommends pages for internal linking based on cosine similarity between embeddings.

    To start, drag and drop or upload a file that contains site data (titles, meta descriptions, H1s-H5s, links, copy, etc.) and embeddings. The file must be in CSV format.
    """)
    return


@app.cell
def _(mo):
    uploader = mo.ui.file(kind='area', filetypes=[".csv", ".parquet"])

    uploader
    return (uploader,)


@app.cell
def _(pl, uploader):
    # Strip titles of separators and brand names
    def clean_titles(df):
        return df.with_columns(
            pl.col('Title').str.replace(' [|-–].*', '')
        )

    # Converts CSV embedding column to an Array dtype
    def convert_str_to_array(df):
        return df.with_columns(
            pl.col("embedding").str.split(",")
            .cast(pl.Array(pl.Float32, 768))
        )

    # Checks if you've uploaded a CSV or a parquet file so it can load it accordingly
    if ".csv" in uploader.name():
        df = pl.read_csv(uploader.contents()).pipe(clean_titles).pipe(convert_str_to_array)
    else:
        df = pl.read_parquet(uploader.contents()).pipe(clean_titles)
    return (df,)


@app.cell
def _(df, mo):
    uploaded_data_table_text = mo.md(r"""
    ## Uploaded data table
    Select the row you want to match against the rest of the pages to find your internal linking opportunities.
    """)

    # This transforms the data into a table with selectable rows
    embeds_table = mo.ui.table(df, selection="single")

    mo.vstack(
        [uploaded_data_table_text, embeds_table]
    )
    return (embeds_table,)


@app.cell
def _(cosine_similarity, df, embeds_table, pl, slider):
    # The `filtered` function generates similarity scores between the row selected in `embeds_table` and every row in the dataframe. It then filters the dataframe by any similarity scores over a threshold, set by the threshold slider

    def filtered(df, threshold):
        return (
            df.with_columns(
                (pl.col("embedding").map_elements(
                    lambda x: cosine_similarity(x, target_vector)
                ) * 100).round(2).alias("Similarity Score")
        )
        .filter((pl.col("Similarity Score") >= slider.value) & (pl.col("URL") != target_url))
        .sort("Similarity Score", descending=True)
        .select(["URL", "Title", "Similarity Score"])
    )

    # `target_url` is the URL from the `embeds_table` selected row and `target_vector` gets the corresponding embedding array

    target_url = embeds_table.value['URL'][0]
    target_vector = df.filter(pl.col("URL") == target_url).select("embedding").item()
    return (filtered,)


@app.cell
def _(mo):
    slider = mo.ui.slider(0, 100, label="Similarity threshold", debounce=False, show_value=True)
    exclude = mo.ui.text(label="URL/subfolder to exclude", debounce=False)
    regex_check = mo.ui.checkbox(label="Check to use regex")
    return exclude, regex_check, slider


@app.cell
def _(exclude, mo, regex_check, slider):
    mo.sidebar(
        mo.Html("""<details><summary><strong>How the parameters work</strong></summary>
    There are three parameter settings to filter your results:
    <ol><li>Use the slider to set the similarity threshold between 0 and 100 (100 is a perfect match, 0 is).</li>
    <li>The textbox allows you to exclude a word or phrase from the URLs.</li>
    <li>To use regex, tick the checkbox below.</li></details>"""),
        [slider, exclude, regex_check]
    )
    return


@app.cell
def _(df, embeds_table, exclude, filtered, mo, pl, regex_check):
    # This displays the final results and checks whether the regex filter is on or off

    if regex_check.value:
        filtered_df = df.pipe(filtered, 0.8).filter(
                ~pl.col("URL").str.contains(exclude.value) if exclude.value else True
            )
    else:
        filtered_df = df.pipe(filtered, 0.8).filter(
                ~pl.col("URL").str.contains(exclude.value, literal=True) if exclude.value else True
            )

    mo.vstack([
        mo.md(f"## Pages similar to: {embeds_table.value['Title'][0]}"),
        mo.md(f"{embeds_table.value['URL'][0]}"),
        filtered_df
    ])
    return


if __name__ == "__main__":
    app.run()
