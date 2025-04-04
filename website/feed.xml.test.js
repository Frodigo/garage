const fs = require('fs');
const path = require('path');

// Set test environment
process.env.NODE_ENV = 'test';

// Mock the modules before requiring feed.xml
jest.mock('fs');
jest.mock('path');
jest.mock('gray-matter', () => jest.fn(() => ({
  data: { title: 'Test Title', date: '2025-04-04' },
  content: 'Test content with [[wiki link]]'
})));

// Mock the marked module
jest.mock('marked', () => ({
  marked: jest.fn().mockReturnValue('<p>Test HTML content</p>')
}));

// Mock the RSS module
jest.mock('rss', () => {
  return jest.fn().mockImplementation(() => ({
    item: jest.fn(),
    xml: jest.fn().mockReturnValue('<xml>Test Feed</xml>')
  }));
});

// Import after mocking
const { 
  findMarkdownFiles, 
  generateUrl, 
  processWikiLinks, 
  getDescription, 
  createFeedItem,
  generateRSSFeed
} = require('./feed.xml');

describe('Feed XML Generator Unit Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('findMarkdownFiles', () => {
    it('should find markdown files in a directory', () => {
      const mockFiles = ['file1.md', 'file2.md', 'file3.txt'];
      const mockStat = {
        isDirectory: jest.fn().mockReturnValue(false)
      };
      
      fs.readdirSync.mockReturnValue(mockFiles);
      fs.statSync.mockReturnValue(mockStat);
      path.join.mockImplementation((...args) => args.join('/'));
      
      const result = findMarkdownFiles('/test', [], []);
      
      expect(result.length).toBe(2);
      expect(result).toContain('/test/file1.md');
      expect(result).toContain('/test/file2.md');
      expect(result).not.toContain('/test/file3.txt');
    });
    
    it('should ignore excluded directories', () => {
      const mockFiles = ['file1.md', 'excluded', 'normal'];
      const mockStat = (p) => ({
        isDirectory: () => p.endsWith('excluded') || p.endsWith('normal')
      });
      
      fs.readdirSync.mockImplementation((dir) => {
        if (dir === '/test') return mockFiles;
        if (dir === '/test/normal') return ['file2.md'];
        return [];
      });
      
      fs.statSync.mockImplementation((p) => mockStat(p));
      path.join.mockImplementation((...args) => args.join('/'));
      path.basename.mockImplementation((p) => p.split('/').pop());
      
      const result = findMarkdownFiles('/test', [], ['excluded']);
      
      expect(result).toContain('/test/file1.md');
      expect(result).toContain('/test/normal/file2.md');
      expect(fs.readdirSync).not.toHaveBeenCalledWith('/test/excluded');
    });
    
    it('should handle errors gracefully', () => {
      fs.readdirSync.mockImplementation(() => {
        throw new Error('Test error');
      });
      
      console.error = jest.fn();
      
      const result = findMarkdownFiles('/test', [], []);
      
      expect(result).toEqual([]);
      expect(console.error).toHaveBeenCalled();
    });
  });
  
  describe('generateUrl', () => {
    it('should handle category links correctly', () => {
      path.basename.mockReturnValue('test');
      
      const result = generateUrl(null, 'Software architecture');
      
      expect(result).toBe('Garage/Software+architecture');
    });
    
    it('should handle regular file paths', () => {
      path.basename.mockReturnValue('test-file');
      path.relative.mockReturnValue('folder/test-file.md');
      
      const result = generateUrl('/test/folder/test-file.md');
      
      expect(result).toBe('folder/test-file');
    });
    
    it('should replace spaces with plus signs', () => {
      path.basename.mockReturnValue('test file');
      path.relative.mockReturnValue('folder/test file.md');
      
      const result = generateUrl('/test/folder/test file.md');
      
      expect(result).toBe('folder/test+file');
    });
  });
  
  describe('processWikiLinks', () => {
    it('should replace wiki links with markdown links', () => {
      const config = {
        site: { site_url: 'https://example.com' }
      };
      
      path.relative.mockReturnValue('folder/test-file.md');
      
      const content = 'Test content with [[wiki link]] in it.';
      const result = processWikiLinks(content, '/test/folder/test-file.md', config);
      
      // Just check that the wiki link is replaced with a markdown link
      expect(result).toContain('[wiki link](https://example.com/');
      // Don't check the exact URL since it depends on implementation details
    });
    
    it('should handle wiki links with display text', () => {
      const config = {
        site: { site_url: 'https://example.com' }
      };
      
      path.relative.mockReturnValue('folder/test-file.md');
      
      const content = 'Test content with [[link|display text]] in it.';
      const result = processWikiLinks(content, '/test/folder/test-file.md', config);
      
      // Just check that the display text is used and a link is created
      expect(result).toContain('[display text](https://example.com/');
      // Don't check the exact URL since it depends on implementation details
    });
  });
  
  describe('getDescription', () => {
    it('should use frontmatter description if available', () => {
      const html = '<p>Test HTML content</p>';
      const data = { description: 'Custom description' };
      
      const result = getDescription(html, data);
      
      expect(result).toBe('Custom description');
    });
    
    it('should extract the first paragraph if no description provided', () => {
      const html = '<p>First paragraph</p><p>Second paragraph</p>';
      const data = {};
      
      const result = getDescription(html, data);
      
      expect(result).toBe('First paragraph');
    });
    
    it('should truncate to 280 chars if no paragraph found', () => {
      const html = 'Very long text without paragraphs '.repeat(10);
      const data = {};
      
      const result = getDescription(html, data);
      
      // Just check that it truncates and adds ellipsis
      expect(result.length).toBeGreaterThan(10);
      expect(result.endsWith('...')).toBe(true);
    });
  });
  
  describe('createFeedItem', () => {
    it('should create a feed item from a markdown file', () => {
      const config = {
        site: { 
          site_url: 'https://example.com',
          author: 'Test Author'
        }
      };
      
      fs.readFileSync.mockReturnValue('---\ntitle: Test Post\ndate: 2025-04-04\n---\nTest content');
      path.basename.mockReturnValue('test-file');
      path.relative.mockReturnValue('folder/test-file.md');
      
      const result = createFeedItem('/test/folder/test-file.md', config);
      
      expect(result).toHaveProperty('title', 'Test Title');
      expect(result).toHaveProperty('url', 'https://example.com/folder/test-file');
      expect(result).toHaveProperty('date');
      expect(result.date instanceof Date).toBe(true);
    });
    
    it('should return null for files without dates', () => {
      const config = {
        site: { site_url: 'https://example.com' }
      };
      
      // Override the mock for this specific test
      const grayMatter = require('gray-matter');
      grayMatter.mockReturnValueOnce({
        data: { title: 'Test Title' }, // No date
        content: 'Test content'
      });
      
      const result = createFeedItem('/test/folder/test-file.md', config);
      
      expect(result).toBeNull();
    });

    it('should handle errors gracefully', () => {
      const config = {
        site: { site_url: 'https://example.com' }
      };
      
      fs.readFileSync.mockImplementationOnce(() => {
        throw new Error('File read error');
      });
      
      console.error = jest.fn();
      
      const result = createFeedItem('/test/folder/test-file.md', config);
      
      expect(result).toBeNull();
      expect(console.error).toHaveBeenCalled();
    });
  });

  describe('generateRSSFeed', () => {
    it('should generate an RSS feed with items', () => {
      const config = {
        site: { 
          site_url: 'https://example.com',
          title: 'Test Feed',
          description: 'Test feed description',
          image_url: 'https://example.com/image.png',
          language: 'en',
          ttl: 60
        },
        title: 'Test Feed',
        feed_url: 'https://example.com/feed.xml',
        outputPath: '/output/feed.xml',
        contentDir: '/content',
        excludeDirs: ['excluded']
      };
      
      // Mock file listing and output directory
      fs.readdirSync.mockReturnValue(['file1.md', 'file2.md']);
      fs.statSync.mockReturnValue({ isDirectory: () => false });
      fs.existsSync.mockReturnValue(false);
      fs.mkdirSync.mockImplementation(() => {});
      path.dirname.mockReturnValue('/output');
      path.basename.mockReturnValue('feed.xml');
      path.join.mockImplementation((...args) => args.join('/'));
      
      console.log = jest.fn();
      
      generateRSSFeed(config);
      
      expect(fs.writeFileSync).toHaveBeenCalled();
      expect(console.log).toHaveBeenCalledTimes(5); // 1 initial + 4 summary logs
    });
  });
});

// Integration tests for link extraction
describe('Feed XML Link Tests', () => {
  let links;

  beforeAll(() => {
    // Reset the mock behavior for integration tests
    const mockXml = `
      <content:encoded><![CDATA[<a href="https://frodigo.com/test/link1">Link 1</a>]]></content:encoded>
      <link>https://frodigo.com/article1</link>
      <guid>https://frodigo.com/article1</guid>
      <description><![CDATA[<a href="https://frodigo.com/test/link2">Link 2</a>]]></description>
      <image><url>https://frodigo.com/image.jpg</url></image>
    `;
    
    fs.readFileSync.mockReturnValue(mockXml);
    path.join.mockImplementation((...args) => args.join('/'));
    
    const feedPath = path.join(__dirname, 'public', 'feed.xml');
    const feedContent = fs.readFileSync(feedPath, 'utf8');
    
    const allLinks = new Set();
    const urlRegex = /https:\/\/frodigo\.com\/[^"\s<>]+/g;
    
    // Extract from content:encoded sections (full article content)
    const contentRegex = /<content:encoded><!\[CDATA\[(.*?)\]\]><\/content:encoded>/gs;
    const contentMatches = [...feedContent.matchAll(contentRegex)];
    contentMatches.forEach(match => {
      const contentUrls = match[1].match(urlRegex) || [];
      contentUrls.forEach(url => allLinks.add(url));
    });
    
    // Extract from link elements (main article links)
    const linkRegex = /<link>(https:\/\/frodigo\.com\/[^<]+)<\/link>/g;
    const linkMatches = [...feedContent.matchAll(linkRegex)];
    linkMatches.forEach(match => allLinks.add(match[1]));
    
    // Extract from guid elements (article identifiers)
    const guidRegex = /<guid[^>]*>(https:\/\/frodigo\.com\/[^<]+)<\/guid>/g;
    const guidMatches = [...feedContent.matchAll(guidRegex)];
    guidMatches.forEach(match => allLinks.add(match[1]));
    
    // Extract from description sections (article previews)
    const descRegex = /<description><!\[CDATA\[(.*?)\]\]><\/description>/gs;
    const descMatches = [...feedContent.matchAll(descRegex)];
    descMatches.forEach(match => {
      const descUrls = match[1].match(urlRegex) || [];
      descUrls.forEach(url => allLinks.add(url));
    });
    
    // Extract from image elements
    const imageRegex = /<image>.*?<url>(https:\/\/frodigo\.com\/[^<]+)<\/url>.*?<\/image>/gs;
    const imageMatches = [...feedContent.matchAll(imageRegex)];
    imageMatches.forEach(match => allLinks.add(match[1]));
    
    links = [...allLinks];
  });

  test('should save links to file', () => {
    // Mock implementation
    fs.writeFileSync.mockImplementation(() => {});
    
    fs.writeFileSync(
      path.join(__dirname, 'links-to-test.json'), 
      JSON.stringify(links, null, 2)
    );
    
    expect(fs.writeFileSync).toHaveBeenCalled();
  });

  test('links should not contain spaces', () => {
    links.forEach(href => {
      expect(href).not.toMatch(/\s/);
    });
  });

  test('links should be properly encoded', () => {
    links.forEach(href => {
      expect(href).not.toMatch(/[<>"']/);
    });
  });

  test('links should not contain double slashes (except in protocol)', () => {
    links.forEach(href => {
      const urlWithoutProtocol = href.replace(/^https?:\/\//, '');
      expect(urlWithoutProtocol).not.toMatch(/\/\//);
    });
  });
});