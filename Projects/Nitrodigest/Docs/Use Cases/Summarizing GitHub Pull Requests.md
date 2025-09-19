---
permalink: projects/nitrodigest/docs/use-cases/summarizing-github-pull-requests
---
You can use Nitrodigest to be up-to-date with changes in repositories you follow. You can use GitHub CLI to fetch pull requests in the terminal. When you have PR data, including description, comments, and diff, you can have a summary of changes for each pull request.

## Prerequisites

Before starting, you'll need:

- Ollama running locally with your preferred model
- **NitroDigest** installed and configured
- **GitHub CLI** installed: [https://cli.github.com/](https://cli.github.com/)

## Authentication to GitHub

GitHub CLI provides a command that allows you to authorize to your account:

```bash
gh auth login
```

You can read more about this command here: [https://cli.github.com/manual/gh_auth_login](https://cli.github.com/manual/gh_auth_login)

## How to select a repository

The GitHub CLI works similarly to Git. The scope of your work is based on the current directory. If you are in the `foo` directory and there is a git repository, this is the repository you will work with.

## Summarizing pull requests from one repository

Let's go to a repository and start summarizing. I will work with the [NLTK repository](https://github.com/nltk/nltk) - one of my favorite repositories.

In the terminal, I use the `cd` command:

```bash
cd OpenSoftware/nltk
```

I can run git status to double-check if I am in a git repository:

```bash
$ (base) frodigo@pop-os:~/OpenSoftware/nltk$ git status
$ On branch develop
$ Your branch is up to date with 'origin/develop'.
```

### List pull requests

Now, let's see open pull requests in this repository:

```bash
gh pr list
```

Output:

```bash
Showing 17 of 17 open pull requests in nltk/nltk

ID     TITLE                                                                           BRANCH                                                         CREATED AT
#3424  Karbi dev                                                                       melur-cu:karbi_dev                                             about 14 hours ago
#3404  Avoid KeyError in langnames.py                                                  ekaf:hotfix-3403                                               about 2 months ago
(...)
```

### Get PR description

The next step is to file the PR description. I use this command:

```bash
gh pr view ekaf:hotfix-3403 --comments > gh-pr-test.md
```

`gh pr view` is a command to view one pull request.

`ekaf:hotfix-3403` is a branch that identifies the PR I want to get. I obtain this branch name from the output of the previous command.

`--comments` flag says that I want to fetch all comments for this pull request.

`> gh-pr-test.md` means that I want to save output from the command to the file

### Get PR diff

Next, let's fetch the PR diff and save it to the same file. To do so, we can use the `gh pr diff` command. Before we save the diff to the file, let's add a few new lines for better formatting:

```bash
printf "\n\n" >> gh-pr-test.md
```

Now, let's add a PR diff to the same file:

```bash
gh pr diff ekaf:hotfix-3403 >> gh-pr-test.md
```

Cool, now we have pull requests' description and diff in the markdown file so that we can summarize it with Nitrodigest:

```bash
nitrodigest gh-pr-test.md
```

Example output:

```bash
---
date: '2025-09-19 07:47:35'
id: gh-pr-test.md
model: mistral
source: file:///home/frodigo/OpenSoftware/nltk/gh-pr-test.md
summary_date: '2025-09-19 07:49:18'
title: gh-pr-test.md
tokens: 665
---

1. PR enhances nltk.langnames module to handle missing inputs gracefully.
     - Adds checks for None and empty strings in tag2q and q2tag functions.
     - Refactors lazy loading of Wikidata mapping and updates inversedictionary generation.
     - Introduces new unit tests in testlangnames.py for invalid and None inputs.
  2. Copilot reviewed the changes and suggested adding more tests for edge cases to ensure expected behavior.
  3. The PR addresses issue 3403 by updating language code conversion functions to use .get() for dictionary lookups, preventing KeyError exceptions.
     - Makes downstream code safer and easier to compose without extra exception handling.
     - Backward-compatible for valid tags/Q-codes.
  4. Suggestions include updating docstrings to clarify that these functions may return None and adding tests for unknown tags/Q-codes to verify the new behavior. 1. Wikidata Conversion Table Loaded Explicitly
    - The table is loaded using `wikibcp47.loadwikiq()`.

  5. Function to get Q-code by Name
     - The function `q2tag(qcode, typfull)` returns a BCP-47 code by given Q-code.

  6. Function to get Name by BCP-47 Code
     - The function `lang2q(name)` returns the corresponding Q-code for a given BCP-47 code.

  7. Inverse Dictionary Creation
     - The function `inversedict(dic)` returns an inverse mapping of a dictionary if it is bijective.

  8. Testing Functions for LangNames
     - A unit test `TestLangNames` is created to check the functions for known and unknown Q-codes and BCP-47 codes.

  9. New File Creation: bnltktestunittestlangnames.py
    - A new file named 'bnltktestunittestlangnames.py' is created for the test case.

  10. Importing Required Modules and Creating Test Case Class
     - The file starts by importing the required modules and creating a test case class `TestLangNames`.

  11. Unit Tests for Tag2Q Function
      - A test `testtag2qknown()` checks if the given BCP-47 code returns the correct Q-code.
      - A test `testtag2qunknown()` checks if it returns None for an unknown tag.

  12. Unit Tests for Q2Tag Function
     - A test `testq2tagknown()` checks if the given Q-code returns the correct BCP-47 code.
     - A test `testq2tagunknown()` checks if it returns None for an unknown Q-code.

  13. Main Function to Run Tests
      - The main function calls `unittest.main()` to run the tests.
```

You can modify summary generated by [Overriding Prompt Templates](Overriding%20Prompt%20Templates.md)

---

## Summarize all open pull requests in a repository

In the previous section, we summarized one specific pull request, and this works perfectly fine. Anyway, sometimes we want to get an overview of what is going on in a repository, and a good way to do this is to review the open pull requests.

Thanks to a small Python script, we can fetch all opened PRs at once to a directory and then summarize the whole directory using Nitrodigest.

### Preparing the script

I wrote a simple script that you can use. Feel free to modify it for your needs. Script is available here: [https://raw.githubusercontent.com/Frodigo/garage/refs/heads/main/Projects/Nitrodigest/src/scripts/fetch_gh_prs.py](https://raw.githubusercontent.com/Frodigo/garage/refs/heads/main/Projects/Nitrodigest/src/scripts/fetch_gh_prs.py)

Once you have downloaded a script, you can use it as is, but it's a good idea to add an alias. I use bash, and I added an alias like this in the `.bashrc`:

```bash
alias fetch-gh-prs="python3 /home/frodigo/Projects/garage/Projects/Nitrodigest/src/scripts/fetch_gh_prs.py"
```

Thanks to this alias, I can easily run a script anywhere on my computer.

### Fetching pull requests

Now, we can fetch all opened pull requests with one command:

```bash
fetch-gh-prs
```

You can customize the directory where PRs will be saved by using the "--dest "flag (default directory is `pull-requests`.

Here is the output of my fetching command:

```bash
$ fetch-gh-prs
$ Saved file pull-requests/Karbi dev.md
$ Saved file pull-requests/Avoid KeyError in langnamespy.md
$ Saved file pull-requests/fix Fixes missing probabilities and unreachable rules in $ PCFG CNF conversion.md
$ Saved file pull-requests/Fix bug ccg logic side effect on lexicon.md
(...)
```

## Summarize pull requests in a directory

Let's summarize all of them:

```bash
nitrodigest pull-requests/
```

When you want to save summary results to a file:

```bash
nitrodigest pull-requests/ > summary.md
```

After a few minutes, I have all PRs summarized:

```bash
$ 2025-09-19 08:05:55,660 - cli.main - INFO - Directory processing complete: 17 of 17 files processed successfully
```

---
Found an issue? Report a bug: <https://github.com/Frodigo/garage/issues/new>

#NitroDigest #Docs #NitroDigestDocs
