namespace WorkshopSystem.Exceptions;

public class RepairsException : Exception
{
    public RepairsException() { }
    public RepairsException(string message) : base(message) { }

    public RepairsException(string message, Exception innerException) : base(message, innerException) { }

}
