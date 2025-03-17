namespace Infrastructure.Prompts;

public static class EmailSummaryPrompt
{
    public static string GetPrompt(string subject, string content, string? partInfo = null)
    {
        var partHeader = !string.IsNullOrEmpty(partInfo) 
            ? $"\nThis is {partInfo} of the email content." 
            : string.Empty;

        return $@"
Analyze and summarize the following email in English, formatting the result as a structured Markdown document.{partHeader}

Format requirements:
1. Start with a level 1 header containing the email subject
2. Add the date as a level 2 header (extract from the email if possible)
3. Add a brief 1-2 sentence overview of the email's purpose in a blockquote
4. Present main points as a bullet list, with sub-bullets for supporting details
5. If action items exist, create a separate 'Action Items' section with checkboxes
6. If deadlines/dates are mentioned, list them in a 'Key Dates' section
7. Use appropriate Markdown formatting for highlighting important elements (bold for critical information, italic for emphasis)
8. If there are any links, references, or contact information, preserve them in Markdown format
9. If the email is a newsletter, include a 'Featured Topics' section
10. Keep the summary concise while capturing all essential information

Important filtering instructions:
- Skip promotional and marketing content that doesn't provide substantial information
- Ignore standard footers, legal disclaimers, and unsubscribe information
- Filter out repetitive boilerplate text
- Omit generic greetings and sign-offs unless they contain relevant context
- Focus only on actionable and informative content
- If the entire email appears to be purely promotional with no substantive information, note this briefly

Email subject: '{subject}'

Content: {content}";
    }
}