using System;
using Microsoft.AspNetCore.Http;
using System.Runtime.Serialization;

namespace WorkshopSystem.Exceptions
{
    public class DiagnosticNotFoundException : Exception
    {
        public DiagnosticNotFoundException(string message) : base(message)
        {
        }

        public DiagnosticNotFoundException(string message, Exception innerException)
            : base(message, innerException)
        {
        }
    }
}