# How the GitHub App works

The [Brethof llms.txt](https://github.com/apps/brethof-llms-txt) app runs the same generator as the Action, on our servers, with our model. You install it, and it does the rest.

## The first file

Within a day of installing, the app opens a pull request that adds `llms.txt` to the root of the repository. The pull request says how the file was made and which model wrote the descriptions. Read it before merging: you know your project, the model only read it.

If the repository already has an `llms.txt`, the app still opens a pull request with its own version, and says so: compare the two and keep the one you prefer. A hand-written file is usually written once and goes stale, while the app's is kept current. To keep yours and stop the app from offering one, set `skip = true` in `.github/llms-txt.toml`, or close the pull request.

## Keeping it current

On the free plan every repository has a weekday, and the pull request tells you which one. On that day, if the docs changed during the week, the app describes the new and changed pages again. Pages that were deleted or moved are fixed on the day it happens, without a model: a moved page keeps its description, because the description follows the page's content.

On the paid plan every change is handled within minutes.

## Pull requests or direct commits

The first file always comes as a pull request. Its description has a checkbox, "Commit future updates directly". Tick it and later updates go straight to your default branch; untick it to go back to pull requests. The box works before and after merging, and `mode = "commit"` or `mode = "pr"` in `.github/llms-txt.toml` does the same. Both kinds of commit are made through GitHub's API, so GitHub signs them and they show as Verified.

## Saying no

Close the app's pull request without merging and it will not open another on that repository. Uninstalling the app stops everything.
