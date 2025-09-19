---
permalink: projects/nitrodigest/docs/summarizing-web-pages
---
## Why summarizing web pages?

Nitrodigest can help you recognize which content is worth your attention and which to skip. The purpose of website summarization isn't to summarize and read a condensed version, but to summarize it to determine whether the content on the page is worth your attention.

## Example

Let's see how it works in action. I will use one of my own posts.

Here is the post: [https://medium.com/gitconnected/how-saying-i-dont-know-can-make-you-a-better-software-engineer-7b85d7c9ed54](https://medium.com/gitconnected/how-saying-i-dont-know-can-make-you-a-better-software-engineer-7b85d7c9ed54)

Before using Nitrodigest, you must obtain the content of this website. You can copy and paste it to a file, but this is not a solution that nerds like you want to use, right?

I faced the same challenge, and to solve it, I created a small program called Nitrowebfetch. It allows us to retrieve content from a website for a given selector and return it in the format we prefer: markdown.

You can read more about Nitrowebfetch [here](https://pypi.org/project/nitrowebfetch-cli/).

Getting content for a specific selector is a good approach because, typically, on a website, you have a lot of noise, such as headers, footers, sidebars, and related articles. We don't need to pass all of that to nitrodigest. We need only to pass the main content of the article that we want to summarize.

Below you can see the command to fetch the content for the website we want to summarize:

```bash
nitrowebfetch https://medium.com/gitconnected/how-saying-i-dont-know-can-make-you-a-better-software-engineer-7b85d7c9ed54
```

After a few seconds, you should see the pretty markdown content of this article. You can easily pipe this content to Nitrodigest using a command like this:

```bash
nitrowebfetch https://medium.com/gitconnected/how-saying-i-dont-know-can-make-you-a-better-software-engineer-7b85d7c9ed54 | nitrodigest
```

Nitrodigest should produce a summary for the website and print it in stdout.

If you want to save the summary to a file, use this command:

```bash
nitrowebfetch https://medium.com/gitconnected/how-saying-i-dont-know-can-make-you-a-better-software-engineer-7b85d7c9ed54 | nitrodigest > summary.md
```

## Command details

This part is responsible for fetching the content of the website:

``` bash
nitrowebfetch <url>
```

Next, we pipe the content to Nitrodigest:

```bash
| nitrodigest
```

If we finish the command here, we will have a summary in the stdout. If you want to have a summary in a file, you need to specify the file you want to save:

```bash
> <file_name>
```

---

The commands I showed you before allow you to summarize the content of web pages. Of course, you can add some parameters to customize the behavior of Nitrowebfetch and Nitrodigest. Follow the links below to get more information:

- [nitrowebfetch documentation](https://frodigo.com/Projects/Nitrowebfetch/README)
- [Overriding Prompt Templates](Overriding%20Prompt%20Templates.md)
- [Using a Custom Configuration](Using%20a%20Custom%20Configuration.md)

---

Found an issue? Report a bug: <https://github.com/Frodigo/garage/issues/new>

#NitroDigest #Docs #NitroDigestDocs
