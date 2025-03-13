using System;
using Microsoft.AspNetCore.Http;
using System.Runtime.Serialization;

namespace WorkshopSystem.Exceptions
{
    public class RepairsNotFoundException : Exception
    {
        public RepairsNotFoundException(string message) : base(message)
        {
        }

        public RepairsNotFoundException(string message, Exception innerException)
            : base(message, innerException)
        {
        }
    }
}
