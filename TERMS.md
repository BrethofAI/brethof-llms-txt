# Terms of service: Brethof llms.txt

Last updated: 6 October 2026

These terms cover the **Brethof llms.txt** GitHub App. The open-source generator and GitHub Action in this repository are covered by their [MIT licence](LICENSE), not by these terms.

## 1. The service

The App writes an `llms.txt` file for the GitHub repositories you install it on, from their README and documentation, and keeps it current as the documentation changes. It is operated by Brethof AI (Poland).

## 2. Your repositories and your file

- Install the App only on repositories you are allowed to change, or that you administer.
- The `llms.txt` the App writes, and every later version of it, belongs to the owner of the repository, under the repository's own licence. We claim no rights in it.
- By default every change arrives as a pull request. Direct commits happen only if you turn them on (the checkbox in the App's pull request, or `mode = "commit"` in `.github/llms-txt.toml`), and you can turn them off at any time.

## 3. AI-written text

The summary and the link descriptions are written by an AI model from your documentation. They can contain mistakes. Read the App's pull requests before merging them; once merged, the file is part of your repository and your responsibility.

## 4. Plans

- The free plan covers public repositories. Its timing (a first file within 24 hours, weekly description updates, same-day fixes for deleted or moved pages) is what we aim for, not a guarantee.
- Paid plans are not on sale yet. When they are, their prices and terms will be added here before anyone is charged.
- We may change or end the free plan. You will always be able to uninstall the App, and the files already in your repositories stay yours.

## 5. Acceptable use

You may not use the App to:
- write to repositories you have no right to change;
- overload the service, or probe or attack it or the repositories of others;
- generate content that is illegal in the EU or in your jurisdiction.

We may stop processing a repository or an account that breaks these rules.

## 6. Ending it

Uninstall the App, or remove a repository from it, at any time from your GitHub settings. What happens to the data we keep is in the [privacy policy](PRIVACY.md). Closing the App's first pull request without merging also ends it for that repository: the App will not open another.

## 7. Liability

The App is provided "as is". To the extent permitted by law, our total liability is limited to the amount you paid us in the 12 months before the claim. Nothing in these terms limits liability that cannot be limited under applicable law, or your statutory consumer rights.

## 8. Changes and law

We may update these terms; material changes are announced in this repository at least 14 days before they take effect. These terms are governed by Polish law. Questions: hello@brethof.ai.
