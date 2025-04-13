using System;

namespace WorkshopSystem.Models
{
    public class DiagnosticData
    {
        public int Id { get; set; }
        public string VehicleVin { get; set; }
        public DateTime Date { get; set; }
        public string Description { get; set; }
        public string Mechanic { get; set; }
    }
}
