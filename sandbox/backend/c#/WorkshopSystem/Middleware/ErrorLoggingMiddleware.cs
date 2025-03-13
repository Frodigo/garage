using System.Net;
using System.Text.Json;
using WorkshopSystem.Exceptions;

namespace WorkshopSystem.Middleware;
public class ErrorLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ErrorLoggingMiddleware> _logger;

    public ErrorLoggingMiddleware(RequestDelegate next, ILogger<ErrorLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (DiagnosticException ex)
        {
            await HandleException(context, ex, "Diagnostic error", StatusCodes.Status500InternalServerError);
        }
        catch (DiagnosticNotFoundException ex)
        {
            await HandleException(context, ex, "Diagnostic not found", StatusCodes.Status404NotFound);
        }
        catch (Exception ex)
        {
            await HandleException(context, ex, "An unexpected error occurred", StatusCodes.Status500InternalServerError);
        }
    }

    private async Task HandleException(HttpContext context, Exception ex, string logMessage, int statusCode)
    {
        _logger.LogError(ex, logMessage);

        context.Response.StatusCode = statusCode;
        context.Response.ContentType = "application/json";

        var errorResponse = new
        {
            Message = ex.Message,
            StatusCode = statusCode
        };

        await context.Response.WriteAsJsonAsync(errorResponse);
    }
}
