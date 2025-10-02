---
permalink: how-and-why-i-moved-my-blog-from-wordpress-to-astro-and-markdown
date: 2025-01-15
title: How and Why I Moved My Blog from WordPress to Astro and Markdown
---
I love writing and have been publishing articles on my blog for several years while constantly working on improving my writing skills. At the same time, as an engineer, I tend to (perhaps unnecessarily) pay attention to the technical aspects of my blog. Initially, my site was a simple WordPress setup. Over time, I expanded it to include support for two languages and the Elementor plugin for easy visual editing of the blog’s layout.

Eventually, this setup became overly complex, and my enjoyment of blogging declined. I decided to abandon WordPress and migrate my blog to a static site built with the Astro framework. In today’s article, I’ll share the journey I took and explain why Astro is an excellent choice for blogging, especially for programmers and web developers. I’ll also show you how I quickly and automatically imported all my WordPress posts into static Markdown files.

## When WordPress Becomes a Burden

WordPress is suitable for 99% o==f== people. It worked for me too, but as I added more plugins, it started running slower and slower.

I used Elementor for customizing my site, but honestly, as a web developer, it’s much easier for me to customize the site’s appearance by editing HTML and CSS rather than using a visual editor.

The growing number of plugins in WordPress negatively impacted the site’s speed for end-users, and I wanted it to be lightning-fast. Plugins also require regular updates. While updates are theoretically automatic, they don’t always work as expected. Once, I updated Elementor, and my site stopped working, costing me several hours of troubleshooting and support calls.

With a large number of posts, the WordPress admin panel became sluggish, and finding anything was a chore. The bilingual setup only made it more cumbersome.

Another factor is that WordPress requires a hosting plan with a database, which incurs costs. In contrast, Astro and Markdown enable a static site, which costs me next to nothing to host. Since I currently earn no income from blogging, eliminating hosting and plugin expenses is a significant advantage.

WordPress also required me to monitor uptime since it’s a dynamically rendered site (server-side rendering). Despite configuring a CDN, there was still occasional downtime.

What finally pushed me to migrate from WordPress to Markdown and Astro was my growing frustration with editing posts in WordPress. It might sound trivial, but the need to log into the panel (requiring an internet connection) started to annoy me. Around that time, I began using Obsidian for note-taking and loved its offline functionality and simple Markdown files. With Obsidian, I can quickly jot something down, which wasn’t the case with WordPress.

## The First Attempt at Migration

While using Obsidian, I discovered an intriguing YouTuber named **Lazar Nikolov**, who demonstrated how to integrate Obsidian with Astro (links to his videos at the end). I had already heard about Astro as a compelling meta-framework for building content-focused websites and apps.

Within a few minutes, I had a proof of concept for a site on Astro with a sample page and my first “Hello World” post. The initial experience was fantastic, but my past experiences taught me to temper my enthusiasm and look for potential weaknesses in the setup.

I had many posts on my blog and worried that I’d need to migrate them manually. Copying the first post from WordPress to Markdown was a nightmare — it required reformatting everything and downloading images separately.

Markdown resonates with me as a programmer. But was that enough of a reason to endure this pain? No.

My blog had around 50 posts in two languages. Some were so outdated that I decided not to migrate them, but I still had about 75 posts to move.

I searched for a WordPress plugin to convert posts to Markdown but couldn’t find anything useful. The thought of manual migration made me want to abandon the process and stick with WordPress.

## A Ray of Hope

I kept searching and discovered a tool that converts WordPress-exported XML content into Markdown:

[https://github.com/lonekorean/wordpress-export-to-markdown](https://github.com/lonekorean/wordpress-export-to-markdown)

A huge thanks to the creators of this tool — it likely saved me dozens of hours of tedious work.

All I had to do was export my WordPress content using the native export feature and run **npx wordpress-export-to-markdown** from the command line. Magic ensued!

The tool generated Markdown files, complete with images, ready for use in my Astro project. I only needed to manually add programming language specifications for code blocks and slightly adjust each post’s properties to match the schema in Astro. Incredible!

## Building a New Tech Stack

Come along — I’ll show you the technologies I used for the new implementation.

### Markdown

As mentioned, I use Obsidian for notes and store all my knowledge there. Transitioning to Markdown simplifies content creation and development for my blog. Thus, the heart of my tech stack, ladies and gentlemen, is: **Markdown**.

While WordPress is great for blogging and Notion excels at note-taking, I value simplicity. That’s why I chose Markdown — it works perfectly for both note-taking and blogging.

### Rendering and Running the Application

I needed a solution to render my Markdown files. While exploring different frameworks for building blogs, I stumbled upon **Astro**. Initially, I was skeptical — another framework for building websites? But after some analysis and testing, I can confidently say that it’s a fantastic tool, especially for developers running a blog. Here’s why:

### Speed and Performance

Astro renders pages server-side and sends the minimal amount of JavaScript to the browser. This translates to lightning-fast page load times. My blog on Astro loads in an instant.

### Flexibility Without Compromise

You can use your favorite tools — React, Vue, or Svelte. Personally, I use **Vue** for more interactive components, while the rest of the site is pure HTML. Thanks to Astro’s island architecture, JavaScript loads only where needed.

### Excellent Content Support

Astro has built-in support for Markdown and MDX. I write posts in Markdown using Obsidian, and it all works out of the box. This allows me to focus on writing without worrying about technical barriers.

### SEO Benefits

Static page generation and minimal JavaScript are a foundation for great SEO. My blog on Astro scores high in Lighthouse without any additional optimization efforts.

### Multilingual Support

On WordPress, I used the paid WPML plugin for multilingual support. In Astro, I wrote a few lines of code to achieve the same functionality — for free. I implemented the structure so that the base domain serves content in English, while the `/pl` subdirectory handles Polish content. The folder structure is as follows:

```bash
- posts/
 - English posts
 - pl/
 - Polish posts
```

These are my two simple functions for detecting the language and retrieving static translations:

```typescript
export function getLangFromUrl(url: URL) {
 const [, lang] = url.pathname.split("/");
 if (lang in ui) return lang as keyof typeof ui;
 return defaultLang;
}

export function useTranslations(lang: keyof typeof ui) {
 return function t(key: keyof (typeof ui)[typeof defaultLang]) {
 return ui[lang][key] || ui[defaultLang];
 };
}
```

I store translations in a simple file:

```json
"header.openMenu": "Open main menu", // English
"header.openMenu": "Otwórz menu główne", // Polish
```

These can be easily used in the project:

```javascript
- -
const lang = getLangFromUrl(Astro.url);
const t = useTranslations(lang);
 - -
<span>{t("header.openMenu")}</span>
```

This setup works flawlessly — for free. Additionally, I use Astro Islands, so some Vue components are included where needed, and this function integrates seamlessly with them.

On WordPress, WPML translations were not only paid but also offered a mediocre experience. With Astro, I can translate Markdown files entirely using any AI tool, making the process more efficient.

### Deployment

In WordPress, deployment was automatic — changes appeared as soon as I saved them in the admin panel.

In my new implementation, the project is built upon pushing changes to the `main` branch. The built project is deployed as a static site on **Vercel**. The build process is fast, although I understand it may slow down as content grows — a reasonable trade-off.

### Testing

For testing, I used **Playwright**. Since I don’t have much to test, I’ve only written tests for the newsletter subscription functionality so far. However, even this small step forward feels significant compared to WordPress, where the only testing was manual and on production.

### Diagrams

In **Obsidian**, diagrams work out of the box with **Mermaid.js**. Integrating Mermaid with Astro was equally straightforward, enabling me to write diagram code that’s automatically rendered as SVGs. I even customized the appearance of these diagrams to match my blog’s theme with just a few lines of configuration and the `remark-mermaid` plugin:

```json
markdown: {
  remarkPlugins: [
    [
      remarkMermaid,
      {
        mermaidConfig: {
          theme: "dark",
          look: "handDrawn",
          themeCSS: ".flowchart { margin-right: 30px; }",
          themeVariables: {
            fontSize: "18px",
            darkMode: true,
            nodeBorder: "#A130E7",
            mainBkg: "#0a1929",
            nodeTextColor: "#fff",
          },
        },
      },
    ],
  ],
},
```

### Frontend Technologies

### Alpine.js vs. Vue.js

Initially, I used Alpine.js for client-side functionality like toggling navigation menus or validating forms. While it worked for simple tasks, I struggled with more complex requirements. Lacking prior experience with Alpine.js, learning it became a chore.

Eventually, I leveraged Astro Islands and switched to Vue.js, a framework I’m highly experienced with, for browser-side functionality.

### Tailwind CSS vs. Sass

At first, I styled the app with Tailwind CSS. However, over time, I switched to Sass. Tailwind’s approach to CSS didn’t resonate with me — I prefer separating structure (HTML) from appearance (CSS). This way, I can add CSS classes in HTML and define their properties in the `<style>` section, making the code more readable for me.

## Lessons Learned from the Migration

### 1. Lightning-Fast Performance

Static sites built with Astro are significantly faster and score higher in PageSpeed Insights. Without additional optimization, my site achieves an 80/100 score on mobile, compared to 30 on WordPress (even after optimizations).

### 2. Markdown Simplicity

Editing content in Markdown is far easier than in WordPress. Finding and modifying anything is a breeze, especially with tools like VS Code, which allow global search and replace. Even with the additional steps of committing, pushing changes, and waiting for the build, the process feels more efficient than WordPress.

### 3. Cost Reduction

I no longer pay for hosting, a database, uptime checks, or WordPress plugins. A static site with my level of traffic incurs almost no costs and ensures 100% uptime.

### 4. Seamless Integration with Obsidian

This new approach tightly integrates my blog with my knowledge and notes stored in Obsidian, making content creation easier and more enjoyable.

### 5. Unexpected Benefits

With everything in Git, I have a complete history of my work, which motivates me and provides a sense of accomplishment. Additionally, I can work offline and publish whenever I have an internet connection — a blessing for anyone familiar with the reliability of Polish trains.

### Challenges

In WordPress, there’s a plugin for everything, whereas in Astro, you often need to implement solutions yourself. Fortunately, most things require a one-time setup.

Collaboration might also be easier on WordPress. If I wanted someone else to contribute content, it would be simpler to find someone familiar with WordPress, as no technical knowledge is required to write there.

## Conclusion

In this article, I shared my journey of migrating my blog from WordPress to Astro, and how Markdown simplified my content creation process. I discussed the challenges I faced with WordPress, from slow performance and editing frustrations to hosting and plugin costs. Then, I detailed how I streamlined the migration process with the right tools.

Static sites built with Astro are fast, cost-effective, and provide greater control over content. Integration with Obsidian further enhances the workflow, making it a fantastic option for tech enthusiasts who value simplicity, speed, and flexibility.

_If you enjoyed this post, follow me for more articles. I’d love to hear about your experiences and perspectives in the comments!_

## Links

- [https://www.youtube.com/watch?v=33Mk-KrWklU&t=610s](https://www.youtube.com/watch?v=33Mk-KrWklU&t=610s)
- [https://www.youtube.com/watch?v=dz3GOp4hN50&t=357s](https://www.youtube.com/watch?v=dz3GOp4hN50&t=357s)
- [https://github.com/lonekorean/wordpress-export-to-markdown](https://github.com/lonekorean/wordpress-export-to-markdown]\(https://github.com/lonekorean/wordpress-export-to-markdown?tab=readme-ov-file%29)
- [https://github.com/remcohaszing/remark-mermaidjs](https://github.com/remcohaszing/remark-mermaidjs)
- [https://obsidian.md/](https://obsidian.md/)
- [https://astro.build/](https://astro.build/)
- [https://playwright.dev/](https://playwright.dev/)
- [https://alpinejs.dev/](https://alpinejs.dev/)
- [https://marcinkwiatkowski.com/blog](https://marcinkwiatkowski.com/blog)

---
*Published: 15/01/2025*  #blog #astrojs #WebDevelopment #WordpressAlternatives #obsidian
