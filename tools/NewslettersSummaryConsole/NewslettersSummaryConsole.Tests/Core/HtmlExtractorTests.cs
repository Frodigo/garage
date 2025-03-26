using Xunit;
using NewslettersSummaryConsole.Core;

namespace NewslettersSummaryConsole.Tests.Core;

public class HtmlExtractorTests
{
    [Fact]
    public void When_GivenSimpleHtml_ShouldExtractPlainText()
    {
        // Arrange
        var html = "<p>Hello <b>World</b></p>";

        // Act
        var result = HtmlExtractor.ExtractText(html);

        // Assert
        Assert.Equal("Hello World", result);
    }

    [Fact]
    public void When_GivenHtmlWithScriptsAndStyles_ShouldRemoveThem()
    {
        // Arrange
        var html = @"
            <style>body { color: red; }</style>
            <p>Hello</p>
            <script>console.log('test');</script>
            <p>World</p>";

        // Act
        var result = HtmlExtractor.ExtractText(html);

        // Assert
        Assert.Equal("Hello World", result);
    }

    [Fact]
    public void When_GivenHtmlWithMultipleSpaces_ShouldNormalizeThem()
    {
        // Arrange
        var html = "<p>Hello    World</p>";

        // Act
        var result = HtmlExtractor.ExtractText(html);

        // Assert
        Assert.Equal("Hello World", result);
    }

    [Fact]
    public void When_GivenHtmlWithHtmlEntities_ShouldDecodeThem()
    {
        // Arrange
        var html = "<p>Hello &amp; World</p>";

        // Act
        var result = HtmlExtractor.ExtractText(html);

        // Assert
        Assert.Equal("Hello & World", result);
    }
} 