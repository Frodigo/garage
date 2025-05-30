---
date: 2025-04-17
title: Why I build my own RSS feed for Obsidian Publish website
---

Obsidian and Obsidian Publish are great tools and they allow you to write and publish content like a nitro. I couldn't imagine what can go wrong when using Obsidian publish. Then after a few weeks I realized what is the weak point that i haven't seen before: **RSS feed**.

Autogenerated RSS feed on Obsidian publish is really simple. I realized it when I talked with my colleague and he asked me about RSS feed. I shared a link with him. He added it to his RSS reader. I saw it. It looked like something hastily written. Just titles, nothing. I felt a bit ashamed.

# TL;DR

- Obsidian Publish's default RSS feed only includes titles and links - no content or descriptions
- After sharing my RSS feed with a colleague, I felt motivated to create a better one
- Built a custom RSS generator that converts Markdown files to feeds with full content
- Implemented special handling for Obsidian's wiki-style links to maintain proper formatting
- Deployed the feeds to Cloudflare Pages with a custom subdomain
- Created two versions: one with all content and one with just recent posts
- Future improvements include code refactoring, category-specific feeds, and simpler hosting via GitHub

---

I investigated why quality of my feed was so bad. It was because in feed generated by Obsidian, there are only two fields for each item: title of an article and link to it.

```xml
<item>
	<title>Historical cryptography algorithms</title>

	<link>
https://frodigo.com/Blog/4.+Historical+cryptography+algorithms
	</link>
</item>
```

So it is not very usable, because someone who uses RSS feeds can only see titles and use link to go to the website.

But what I like the most when I use RSS feeds is to have possibility to read content without need to go outside.

So for me proper RSS feed item looks like this:

```xml
<item>
	<title>
		<![CDATA[ Historical cryptography algorithms ]]>
	</title>

	<description>
		# short description like first paragraph
	</description>

	<link>
https://frodigo.com/Blog/4.+Historical+cryptography+algorithms
	</link>

	<guid isPermaLink="false">
	https://frodigo.com/Blog/4.+Historical+cryptography+algorithms
	</guid>

	<pubDate>Fri, 28 Mar 2025 00:00:00 GMT</pubDate>

	<content:encoded>
		# full content here so I can read it in my RSS reader
	</content:encoded>

</item>
```

In this example you can see that there is description field that shows something like excerpt. Also there is a content field which contains a full content of an article.

I tried to find how to implement something like this using Obsidian publish, but I didn't find a way.

So I started to thinking how to implement it by myself.

And I came up with this idea:

- create RSS feed from my markdown files
- deploy it somewhere
- add link to it on my website

---

## Creating RSS feed

In my astro blog I had a script in JS that generates RSS feed so I have used it as starting point

I needed to adjust it a little bit. I needed to implement support for links in Obsidian Wiki format like `[[link]]` or even `[[this is link|this is a text]]`.

Also I wanted to have an option to specify which content should be in feed and which not. On my website I have a few pages that can be considered as blog article (like this one). Besides, I have a lot of content that is just my Notes, and I don't want to spam people with anything that comes to mind.

I didn't have to much time so I used Cursor to adjust this script to my needs.

I was disappointment about results. Cursor was not able to implement link formatting in a acceptable way. Cursor generated hundreds of lines of code for simple feature.

In addition, when I asked it about writing tests, cursor started do things like a drunk programmer.

So I landed with an overcomplicated solution. But it works.

How it works:

- **Markdown in → RSS out**: scans my project for dated `.md` notes and turns them into two RSS files
- **Obsidian link handling**: understands `[[Wiki Links]]`, cleans up internal URLs, and keeps external links unchanged.
- **Auto metadata**: pulls title, date, description, categories, and optional hero image from each file’s front‑matter.
- **Feed hygiene**: sorts by date, skips undated posts, and embeds full HTML content in `<content:encoded>`
- **Post‑build sanity check**: extracts every internal link from the feed and writes them to `links-to-test.json` for automated link‑testing.

This is the full implementation: [https://gist.github.com/Frodigo/bbcf18db7e431cfcbb31f6fb13dd9cd6](https://gist.github.com/Frodigo/bbcf18db7e431cfcbb31f6fb13dd9cd6)

Here is the most interesting part:

```javascript
// --- Link‑handling magic ---
function configureMarkedRenderer() {
  const renderer = new marked.Renderer();

  renderer.link = (href, title, text) => {
    // Extract URL from href if it's an object
    const hrefStr =
      typeof href === "object" && href !== null
        ? href.href || href.url || "#"
        : String(href || "");

    // Extract text content if it's an object
    const textStr =
      typeof text === "object" && text !== null
        ? text.text || text.title || hrefStr
        : String(text || hrefStr);

    // Handle wiki links
    if (hrefStr.startsWith("[[")) {
      const linkText = hrefStr.slice(2, -2);
      const url = generateUrl(null, linkText);
      return `<a href="${url}">${textStr}</a>`;
    }

    // For regular links, extract the last part of the URL for the text and decode it
    if (hrefStr.startsWith("https://frodigo.com/")) {
      const lastPart = hrefStr.split("/").pop();
      const decodedText = decodeURIComponent(lastPart.replace(/\+/g, " "));
      return `<a href="${hrefStr}">${decodedText}</a>`;
    }

    // For regular links, ensure proper formatting
    return `<a href="${hrefStr}">${textStr}</a>`;
  };

  marked.setOptions({
    renderer,
    mangle: false,
    headerIds: false,
  });
}

function processWikiLinks(html, filePath, config) {
  return html.replace(/\[\[(.*?)\]\]/g, (_, link) => {
    const [target, label = target] = link.split("|");
    const url = `${config.site.site_url}/${generateUrl(null, target)}`;
    return `<a href="${url}">${label}</a>`;
  });
}
```

(funny thing: when I added this snippet to codebase, I needed immediately fix the generator because it generated links from the code snippet...)

These two functions are responsible for handling and parsing links.

`processWikiLinks()` runs over the freshly rendered HTML and turns any remaining `[[Wiki Link|Label]]` syntax into fully qualified site URL.

I didn't trust to this Cursor generated code and I needed to created a e2e tests that checks that all links in generated feed are ok.

I set up Playwright for that and wrote simple test: [https://gist.github.com/Frodigo/e1577910f92c0619b21b7d1c9de4c5a1](https://gist.github.com/Frodigo/e1577910f92c0619b21b7d1c9de4c5a1)

---

## Deploying RSS feed

I tried to upload generated xml files to Obsidian Publish "server", but it is not possible

So I decided to create a simple static website (used CLaudflare pages for that) and I deployed generated feeds there.

Also I created a Github action that automatically generate feeds and deploy them to Cloudflare: [https://gist.github.com/Frodigo/a129e1914fea25156dfd2907d9a65940](https://gist.github.com/Frodigo/a129e1914fea25156dfd2907d9a65940)

In addition I set up subdomains and it the end I have two RSS feeds available:

- All items: [https://rss.frodigo.com/feed.xml](https://rss.frodigo.com/feed.xml)
- Recent 10 items: [https://rss.frodigo.com/feed.recent.xml](https://rss.frodigo.com/feed.recent.xml)

## Showing feeds on my Obsidian page

This was an easy one. I have just written a section on my homepage and added links there.

---

## Wrap up

I needed a few hours to generate this feed and deploy it to the server and now I have my RSS feed.

I see some potential improvement that I can make:

1. Before everything I have to refactor the code, because I feel it can be 5 times more simple when human writes it.
2. I want to have separate feeds for categories
3. I realized that instead of deploying generated feed to Cloudflare I can just generate it and keep in version control. My repository is public so I can just use a raw version of file from Github and it should work

All of these items I will do before I die. If so, I will write about them in the separate article.

I am wondering how to do this changes in a way that someone else can have such a nice RSS feed on their Obsidian page. Maybe Obsidian plugin? If you think is interesting, let me know!

---

_Written by Marcin Kwiatkowski at 17.04.2025 in Poland._

#RSS #Obsidian #ObsidianPublish #WebDevelopment #ContentSyndication #JavaScript #StaticSite #BloggingTools #WebAutomation #Markdown #GitHubActions #CloudflareSites #KnowledgeManagement #DigitalGarden #RSSFeeds #ContentCreation #WebsiteCustomization #AIAssistants #ProgrammingChallenge #PersonalProject #FrontendDevelopment #NodeJS #Git #CI/CDtools #Cloudflare #Tutorial #CaseStudy #ProjectSetup #Intermediate #APISecurity #AutomatedTesting
