# Quality Gates

## Evidence Gate

Block publishing if:
- the main claim is unsupported
- a paper was only read from abstract/README/snippet
- a GitHub repo article only used README when code/issues/examples matter
- a proxy metric is presented as business value
- source dates are uncertain for current topics

## Writing Gate

Block or revise if:
- opening does not tell the reader why to care
- title is stale or low-signal
- paragraph rhythm feels AI-generated
- article overuses English jargon
- reader cannot tell who the article is for
- evidence appears as summary dump rather than argument support

## Visual Gate

Required:
- `imgs/outline.md` exists for generated body visuals
- each generated image has a saved prompt file
- prompt files include Baoyu sections (`LAYOUT`, `ZONES`/`STRUCTURE`, `LABELS`, `COLORS`, `STYLE`, `ASPECT`)
- body visuals explain article-specific ideas
- original evidence figures/screenshots are preserved where needed

Block publishing if generated images are only decorative or generic.

## Markdown Gate

Run `validate_article_assets.py`.

Checks:
- article exists
- frontmatter includes title
- cover image exists
- all markdown image paths exist
- required visual artifacts exist when generated body visuals are present

## Publishing Gate

Run `preflight.ps1`.

Checks:
- `bun`, `node`, `python`, `ssh` available
- WeChat env file exists if API publishing
- remote API SSH key exists when configured
- project publish wrapper or Baoyu API script exists

## Final Gate

Final response must not hide residual risk. If something was inferred, say so.
