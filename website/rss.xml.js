const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { marked } = require('marked');
const RSS = require('rss');

const config = {
  site: {
    title: "Marcin Kwiatkowski's Blog",
    description: "Blog about software engineering.",
    site_url: 'https://frodigo.com',
    feed_url: 'https://frodigo.com/rss.xml',
    image_url: 'https://frodigo.com/favicon-32.png',
    language: 'en',
    ttl: 60
  },
  contentDir: path.join(__dirname),
  outputPath: path.join(__dirname, 'public', 'rss.xml')
};

// Create RSS feed
const feed = new RSS({
  title: config.site.title,
  description: config.site.description,
  site_url: config.site.site_url,
  feed_url: config.site.feed_url,
  image_url: config.site.image_url,
  language: config.site.language,
  ttl: config.site.ttl,
  pubDate: new Date()
});

const outputDir = path.dirname(config.outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

function generateRSSFeed() {
  const markdownFiles = fs.readdirSync(config.contentDir)
    .filter(file => file.endsWith('.md'));
  
  markdownFiles.forEach(file => {
    const filePath = path.join(config.contentDir, file);
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    const { data, content } = matter(fileContent);
    
    if (!data.date) {
      console.warn(`Skipping ${file}: missing required frontmatter (title or date)`);
      return;
    }
    
    // Preprocess content to convert wiki-style links directly to HTML
    const processedContent = content.replace(/\[\[(.*?)\]\]/g, (match, text) => {
      // Handle links with pipe character (|)
      if (text.includes('|')) {
        const [link, displayText] = text.split('|');
        const slug = link.toLowerCase().replace(/\s+/g, '-');
        return `<a href="${config.site.site_url}/${slug}">${displayText}</a>`;
      }
      // Handle regular wiki links
      const slug = text.toLowerCase().replace(/\s+/g, '-');
      return `<a href="${config.site.site_url}/${slug}">${text}</a>`;
    });
    
    const htmlContent = marked(processedContent);
    
    const slug = data.slug || file.replace(/\.(md)$/, '');
    const url = `${config.site.site_url}/${slug}`;
    
    feed.item({
      title: slug,
      description: data.description || htmlContent.substring(0, 280) + '...',
      url: url,
      guid: url,
      categories: data.categories || [],
      author: config.site.author,
      date: new Date(data.date),
      enclosure: data.image ? {
        url: data.image.startsWith('http') ? data.image : `${config.site.site_url}/${data.image}`,
        type: 'image/jpeg'
      } : undefined,
      custom_elements: [
        { 'content:encoded': { _cdata: htmlContent } }
      ]
    });
  });
  
  fs.writeFileSync(config.outputPath, feed.xml({ indent: true }));
  console.log(`RSS feed generated at ${config.outputPath}`);
}

generateRSSFeed();