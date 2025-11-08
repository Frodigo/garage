const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");
const { marked } = require("marked");
const RSS = require("rss");

/**
 * Configure marked renderer with custom link handling
 */
function configureMarkedRenderer() {
  try {
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

      // Return standard link
      return `<a href="${hrefStr}">${textStr}</a>`;
    };

    marked.setOptions({
      renderer,
      mangle: false,
      headerIds: false,
    });

    return renderer;
  } catch (error) {
    // Handle error gracefully
    console.warn("Error configuring marked renderer:", error.message);
    return null;
  }
}

// Base configuration
const baseConfig = {
  site: {
    title: "The garage",
    description:
      "Garage for engineers. Place where you can find notes, tutorials, experiments, concepts explanation and more.",
    site_url: "https://frodigo.com",
    image_url: "https://frodigo.com/favicon-32.png",
    language: "en",
    ttl: 60,
  },
  contentDir: path.join(__dirname, "..", ".."),
  excludeDirs: [
    "node_modules",
    ".git",
    ".github",
    "public",
    "dist",
    ".next",
    "priv",
    "src",
    "venv",
  ],
};

// Feed-specific configurations
const feedConfigs = {
  all: {
    ...baseConfig,
    outputPath: path.join(__dirname, "public", "feed.xml"),
    feed_url: "https://rss.frodigo.com/feed.xml",
    title: "The garage - All posts",
  },
  recent: {
    ...baseConfig,
    outputPath: path.join(__dirname, "public", "feed.recent.xml"),
    feed_url: "https://rss.frodigo.com/feed.recent.xml",
    maxItems: 10,
    title: "The garage - Recent posts",
  },
};

// Initialize marked renderer (not in test environment)
if (process.env.NODE_ENV !== "test") {
  configureMarkedRenderer();
}

/**
 * Recursively find all markdown files in the given directory
 * @param {string} dir - Directory to search
 * @param {Array<string>} fileList - Accumulator for found files
 * @param {Array<string>} excludeDirs - Directories to exclude from search
 * @returns {Array<string>} List of markdown file paths
 */
function findMarkdownFiles(dir, fileList = [], excludeDirs) {
  try {
    const files = fs.readdirSync(dir);

    files.forEach((file) => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        const dirName = path.basename(filePath);
        if (excludeDirs.includes(dirName)) {
          return;
        }
        findMarkdownFiles(filePath, fileList, excludeDirs);
      } else if (file.endsWith(".md")) {
        fileList.push(filePath);
      }
    });

    return fileList;
  } catch (error) {
    console.error(`Error finding markdown files in ${dir}:`, error);
    return fileList;
  }
}

/**
 * Generate a normalized URL from file path
 * @param {string} filePath - Path to the file
 * @returns {string} Generated URL
 */
function generateUrl(filePath) {
  const relativePath = path.relative(baseConfig.contentDir, filePath);
  return relativePath
    .replace(/\.(md)$/, "")
    .replace(/\\/g, "/")
    .replace(/\s+/g, "+");
}

/**
 * Extract description from HTML content
 * @param {string} html - HTML content
 * @param {object} data - Frontmatter data
 * @returns {string} Description text
 */
function getDescription(html, data) {
  // Use frontmatter description if available
  if (data.description) return data.description;

  // Remove all links but keep their text content
  const textWithoutLinks = html.replace(/<a[^>]*>(.*?)<\/a>/g, "$1");

  // Try to get first paragraph
  const firstParagraph = textWithoutLinks.match(/<p>(.*?)<\/p>/);
  if (firstParagraph) {
    return firstParagraph[1];
  }

  // If no paragraph found, take first 280 characters
  return textWithoutLinks.substring(0, 280) + "...";
}

/**
 * Create a feed item from a markdown file
 * @param {string} filePath - Path to the markdown file
 * @param {object} config - Feed configuration
 * @returns {object|null} Feed item or null if skipped
 */
function createFeedItem(filePath, config) {
  try {
    const fileContent = fs.readFileSync(filePath, "utf8");
    const { data, content } = matter(fileContent);

    // Skip files without dates
    if (!data.date) {
      return null;
    }

    // Convert markdown to HTML
    const renderer = new marked.Renderer();
    renderer.link = (href, title, text) => {
      const hrefStr =
        typeof href === "object" && href !== null
          ? href.href || href.url || "#"
          : String(href || "");

      const textStr =
        typeof text === "object" && text !== null
          ? text.text || text.title || hrefStr
          : String(text || hrefStr);

      return `<a href="${hrefStr}">${textStr}</a>`;
    };

    marked.setOptions({ renderer, mangle: false, headerIds: false });
    const htmlContent = marked(content);

    const url = `${config.site.site_url}/${generateUrl(filePath)}`;

    return {
      title: data.title || path.basename(filePath, ".md"),
      description: getDescription(htmlContent, data),
      url: url,
      guid: url,
      categories: data.categories || [],
      author: config.site.author,
      date: new Date(data.date),
      enclosure: data.image
        ? {
            url: data.image.startsWith("http")
              ? data.image
              : `${config.site.site_url}/${data.image}`,
            type: "image/jpeg",
          }
        : undefined,
      custom_elements: [{ "content:encoded": { _cdata: htmlContent } }],
    };
  } catch (error) {
    console.error(`Error processing file ${filePath}:`, error);
    return null;
  }
}

/**
 * Generate an RSS feed with the given configuration
 * @param {object} config - Feed configuration
 */
function generateRSSFeed(config) {
  console.log(`\nGenerating ${path.basename(config.outputPath)}...`);

  // Create RSS feed
  const feed = new RSS({
    title: config.title,
    description: config.site.description,
    site_url: config.site.site_url,
    feed_url: config.feed_url,
    image_url: config.site.image_url,
    language: config.site.language,
    ttl: config.site.ttl,
    pubDate: new Date(),
  });

  // Create output directory if it doesn't exist
  const outputDir = path.dirname(config.outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Find markdown files and create feed items
  const markdownFiles = findMarkdownFiles(
    config.contentDir,
    [],
    config.excludeDirs
  );
  const feedItems = [];
  let skippedCount = 0;

  markdownFiles.forEach((filePath) => {
    const feedItem = createFeedItem(filePath, config);
    if (feedItem) {
      feedItems.push(feedItem);
    } else {
      skippedCount++;
    }
  });

  // Sort by date (newest first)
  feedItems.sort((a, b) => b.date - a.date);

  // Add items to feed (limiting if necessary)
  const itemsToAdd = config.maxItems
    ? feedItems.slice(0, config.maxItems)
    : feedItems;
  itemsToAdd.forEach((item) => feed.item(item));

  // Write feed to file
  fs.writeFileSync(config.outputPath, feed.xml({ indent: true }));

  // Log results
  console.log(`✓ Found ${feedItems.length} posts with dates`);
  console.log(
    `✓ Added ${itemsToAdd.length} ${
      config.maxItems ? "most recent " : ""
    }posts to the feed`
  );
  console.log(`✓ Skipped ${skippedCount} posts without dates`);
  console.log(`✓ Feed saved to ${path.basename(config.outputPath)}\n`);
}

/**
 * Check if a URL looks valid (not containing array notation or other invalid patterns)
 * @param {string} url - URL to validate
 * @returns {boolean} True if URL looks valid
 */
function isValidUrl(url) {
  // Extract the path part after the domain
  const pathMatch = url.match(/https:\/\/frodigo\.com\/(.+)$/);
  if (!pathMatch) {
    return false;
  }
  const path = pathMatch[1];

  // Filter out URLs that are just numbers (likely extracted from array notation like [10, 20, 30])
  if (/^\d+$/.test(path)) {
    return false;
  }

  // Filter out URLs that contain array notation patterns
  if (/\[.*?\]/.test(url)) {
    return false;
  }
  // Filter out URLs that start with numbers followed by commas (array elements)
  if (/\/\d+,\+/.test(url)) {
    return false;
  }
  // Filter out URLs ending with array-like patterns
  if (/,\+\d+[,\]]/.test(url)) {
    return false;
  }
  // Filter out other invalid patterns
  if (
    url.includes("...") ||
    url.includes("undefined") ||
    url.includes("link") ||
    url.includes("Wiki") ||
    url.includes("&quot;")
  ) {
    return false;
  }
  return true;
}

/**
 * Extract links from RSS feed XML content
 * @param {string} feedContent - RSS feed XML content
 * @returns {Set<string>} Set of unique links
 */
function extractLinksFromFeed(feedContent) {
  const allLinks = new Set();
  // More restrictive regex: stop at brackets, parentheses, and other invalid URL characters
  // Also stop at common punctuation that shouldn't be in URLs
  const urlRegex = /https:\/\/frodigo\.com\/[^"\s<>\[\](){}|\\^`]+/g;

  // First, remove code blocks to avoid processing links within them
  // Also remove inline code with backticks
  let contentWithoutCodeBlocks = feedContent.replace(
    /<pre><code>[\s\S]*?<\/code><\/pre>/gi,
    ""
  );
  // Remove inline code elements
  contentWithoutCodeBlocks = contentWithoutCodeBlocks.replace(
    /<code>[\s\S]*?<\/code>/gi,
    ""
  );

  // Extract from content:encoded sections (full article content)
  const contentRegex =
    /<content:encoded><!\[CDATA\[(.*?)\]\]><\/content:encoded>/gs;
  const contentMatches = [...contentWithoutCodeBlocks.matchAll(contentRegex)];
  contentMatches.forEach((match) => {
    const contentUrls = match[1].match(urlRegex) || [];
    contentUrls.forEach((url) => {
      // Filter out invalid links using the validation function
      if (isValidUrl(url)) {
        allLinks.add(url);
      }
    });
  });

  // Extract from link elements (main article links)
  const linkRegex = /<link>(https:\/\/frodigo\.com\/[^<]+)<\/link>/g;
  const linkMatches = [...contentWithoutCodeBlocks.matchAll(linkRegex)];
  linkMatches.forEach((match) => {
    const url = match[1];
    if (isValidUrl(url)) {
      allLinks.add(url);
    }
  });

  // Extract from guid elements (article identifiers)
  const guidRegex = /<guid[^>]*>(https:\/\/frodigo\.com\/[^<]+)<\/guid>/g;
  const guidMatches = [...contentWithoutCodeBlocks.matchAll(guidRegex)];
  guidMatches.forEach((match) => {
    const url = match[1];
    if (isValidUrl(url)) {
      allLinks.add(url);
    }
  });

  // Extract from description sections (article previews)
  const descRegex = /<description><!\[CDATA\[(.*?)\]\]><\/description>/gs;
  const descMatches = [...contentWithoutCodeBlocks.matchAll(descRegex)];
  descMatches.forEach((match) => {
    const descUrls = match[1].match(urlRegex) || [];
    descUrls.forEach((url) => {
      if (isValidUrl(url)) {
        allLinks.add(url);
      }
    });
  });

  // Extract from image elements
  const imageRegex =
    /<image>.*?<url>(https:\/\/frodigo\.com\/[^<]+)<\/url>.*?<\/image>/gs;
  const imageMatches = [...contentWithoutCodeBlocks.matchAll(imageRegex)];
  imageMatches.forEach((match) => {
    const url = match[1];
    if (isValidUrl(url)) {
      allLinks.add(url);
    }
  });

  return allLinks;
}

/**
 * Save extracted links to a JSON file
 * @param {Set<string>} links - Set of links to save
 * @param {string} outputPath - Path where to save the file
 */
function saveLinksToFile(links, outputPath) {
  const linksArray = [...links];
  console.log("Saving links to file:", outputPath);
  console.log("Current directory:", process.cwd());
  console.log("Number of links to save:", linksArray.length);

  // Ensure the directory exists
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    console.log("Creating directory:", dir);
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.writeFileSync(outputPath, JSON.stringify(linksArray, null, 2));
  console.log(
    `✓ Saved ${linksArray.length} links to ${path.basename(outputPath)}`
  );
}

// Main execution - only run if this is the main module (not in tests)
if (require.main === module) {
  console.log("🔄 Generating RSS feeds...");

  // Generate all configured feeds
  Object.values(feedConfigs).forEach((config) => {
    generateRSSFeed(config);
  });

  // Extract links from the main feed and save them
  const mainFeedPath = path.join(__dirname, "public", "feed.xml");
  console.log("Reading feed from:", mainFeedPath);

  if (!fs.existsSync(mainFeedPath)) {
    console.error("Error: Feed file not found at", mainFeedPath);
    process.exit(1);
  }

  const mainFeedContent = fs.readFileSync(mainFeedPath, "utf8");
  const links = extractLinksFromFeed(mainFeedContent);

  const linksFilePath = path.join(__dirname, "links-to-test.json");
  console.log("Saving links to:", linksFilePath);
  saveLinksToFile(links, linksFilePath);

  console.log("✨ All feeds generated successfully!");
}

// Export for testing
module.exports = {
  findMarkdownFiles,
  generateUrl,
  getDescription,
  createFeedItem,
  generateRSSFeed,
  extractLinksFromFeed,
  isValidUrl,
};
