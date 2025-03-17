using HtmlAgilityPack;

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

        // Clean text
        text = System.Text.RegularExpressions.Regex.Replace(text, @"\s+", " ");
        text = text.Trim();

        return text;
    }
} 