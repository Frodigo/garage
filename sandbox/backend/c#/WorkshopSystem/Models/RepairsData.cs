using System;

namespace WorkshopSystem.Models
{
    public class RepairsData
    {
        public int Id { get; set; }
        public string VehicleVin { get; set; }
        public DateTime Date { get; set; }
        public string Description { get; set; }
        public string Mechanic { get; set; }
        public decimal Cost { get; set; }
        public RepairStatus Status { get; set; }
        public string Notes { get; set; }
    }
}
