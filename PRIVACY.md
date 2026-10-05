# Privacy policy: Brethof llms.txt

Last updated: 6 October 2026

This policy covers the **Brethof llms.txt** GitHub App. The open-source generator and GitHub Action in this repository run on your own machines or runners and send nothing to us.

## 1. Who we are

Brethof llms.txt is operated by Brethof AI, based in Poland (EU). Contact: hello@brethof.ai.

## 2. What the App can access

When you install the App, GitHub grants it these permissions on the repositories you choose:
- read access to metadata;
- read and write access to code and pull requests.

GitHub sends the App events about installations, pushes, pull requests and Marketplace plans.

## 3. What we do with your repository

For each job, our worker makes a temporary copy of only the files the generator reads: Markdown, MDX, reStructuredText, AsciiDoc and notebook files, navigation files such as `mkdocs.yml`, and package manifests such as `pyproject.toml` or `package.json`. It does not fetch your source code files (from notebooks it reads only the text cells). The copy is deleted when the job ends.

An AI model reads excerpts of those files (the start of the README and the start of each linked page) and writes the summary and the link descriptions:
- **Free plan:** a model running on our own hardware. Nothing is sent to any third party.
- **Paid plan:** GLM through Ollama Cloud. Ollama states that prompt and response data is never logged or trained on. Its servers are mainly in the United States, with Europe and Singapore used for extra capacity, so on the paid plan these excerpts may be processed outside the EU.

The App then writes `llms.txt` to your repository, as a pull request or, if you choose it, as a direct commit.

## 4. What we store

On our server we keep, for each repository the App covers:
- the account and repository name, whether it is private, its default branch, and your plan;
- the generated summary and link descriptions, each with a short hash of the page it describes (so that unchanged pages are not described again);
- the commit the App last processed, the pull request it opened, and your choice of pull requests or direct commits;
- a record of each job (time, outcome, model token counts) and of the events GitHub sent.

We do not store your source code, the contents of your documentation, or anything about the people who use your repository.

## 5. How long

- **Uninstalling the App** (or removing a repository from it) deletes the generated descriptions, the processed commit and the pull-request link for that repository. We keep only its name, marked as removed.
- **Job and event records** are deleted after 12 months.
- To have everything about your account deleted sooner, email hello@brethof.ai.

## 6. Who else is involved

- **GitHub**, which hosts your repository and delivers the App's events.
- **Cloudflare**, which carries traffic to our server.
- **Ollama Cloud**, on the paid plan only, for the AI model.
- **The provider that hosts our server.**

We do not sell your data, and we do not use it to train models. There is no tracking and there are no cookies.

## 7. Your rights (GDPR)

You have the right to access, rectify, export and erase your data, to restrict or object to processing, and to lodge a complaint with a supervisory authority (in Poland: UODO). Email hello@brethof.ai.

## 8. Changes

We will update this page when the App changes what it accesses or stores, and change the date at the top.
