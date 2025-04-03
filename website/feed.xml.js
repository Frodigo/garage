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
    feed_url: 'https://frodigo.com/feed.xml',
    image_url: 'https://frodigo.com/favicon-32.png',
    language: 'en',
    ttl: 60
  },
  contentDir: path.join(__dirname),
  outputPath: path.join(__dirname, 'public', 'feed.xml'),
  maxItems: 15, 
  excludeDirs: ['node_modules', '.git', '.github', 'public', 'dist', '.next']
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

function findMarkdownFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      const dirName = path.basename(filePath);
      if (config.excludeDirs.includes(dirName)) {
        return;
      }
      findMarkdownFiles(filePath, fileList);
    } else if (file.endsWith('.md')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

function generateRSSFeed() {
  const markdownFiles = findMarkdownFiles(config.contentDir);
  
  const feedItems = [];
  
  markdownFiles.forEach(filePath => {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    const { data, content } = matter(fileContent);
    
    if (!data.date) {
      console.warn(`Skipping ${filePath}: missing required frontmatter (date)`);
      return;
    }
    
    const processedContent = content.replace(/\[\[(.*?)\]\]/g, (match, text) => {
      if (text.includes('|')) {
        const [link, displayText] = text.split('|');
        const slug = link.toLowerCase().replace(/\s+/g, '-');
        return `<a href="${config.site.site_url}/${slug}">${displayText}</a>`;
      }
      const slug = text.toLowerCase().replace(/\s+/g, '-');
      return `<a href="${config.site.site_url}/${slug}">${text}</a>`;
    });
    
    const htmlContent = marked(processedContent);
    
    const relativePath = path.relative(config.contentDir, filePath);
    const fileSlug = relativePath.replace(/\.(md)$/, '').replace(/\\/g, '/');
    
    const slug = data.slug || fileSlug;
    const url = `${config.site.site_url}/${slug}`;
    
    feedItems.push({
      title: data.title || slug,
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
  
  feedItems.sort((a, b) => b.date - a.date);
  
  const limitedItems = feedItems.slice(0, config.maxItems);
  
  limitedItems.forEach(item => {
    feed.item(item);
  });
  
  fs.writeFileSync(config.outputPath, feed.xml({ indent: true }));
  console.log(`RSS feed generated at ${config.outputPath}`);
  console.log(`Added ${limitedItems.length} of ${feedItems.length} total posts to RSS feed`);
  console.log(`Excluded directories: ${config.excludeDirs.join(', ')}`);
}

generateRSSFeed();
