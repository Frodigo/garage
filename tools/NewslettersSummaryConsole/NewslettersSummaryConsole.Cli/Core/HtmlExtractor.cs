using HtmlAgilityPack;
using System.Text.RegularExpressions;

namespace NewslettersSummaryConsole.Core;

public static class HtmlExtractor
{
    public static string ExtractText(string html)
    {
        var doc = new HtmlDocument();
        doc.LoadHtml(html);

        // Remove scripts and styles
        var scripts = doc.DocumentNode.SelectNodes("//script");
        var styles = doc.DocumentNode.SelectNodes("//style");
        
        if (scripts != null)
        {
            foreach (var script in scripts)
            {
                script.Remove();
            }
        }

        if (styles != null)
        {
            foreach (var style in styles)
            {
                style.Remove();
            }
        }

        // Extract text
        var text = doc.DocumentNode.InnerText;

        // Decode HTML entities
        text = System.Web.HttpUtility.HtmlDecode(text);

        // Clean text
        text = Regex.Replace(text, @"\s+", " "); // Replace multiple spaces with single space
        text = Regex.Replace(text, @"[^\x20-\x7E\n\r]", ""); // Remove non-printable characters
        text = Regex.Replace(text, @"\n\s*\n", "\n\n"); // Replace multiple newlines with double newline
        text = text.Trim();

        return text;
    }
} 