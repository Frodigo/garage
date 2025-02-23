namespace WorkshopSystem.Exceptions;

public class DiagnosticException : Exception
{
    public DiagnosticException() { }
    public DiagnosticException(string message) : base(message) { }

    public DiagnosticException(string message, Exception innerException) : base(message, innerException) { }

}