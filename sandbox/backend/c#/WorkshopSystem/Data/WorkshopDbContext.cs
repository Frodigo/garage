using Microsoft.EntityFrameworkCore;
using WorkshopSystem.Models;

namespace WorkshopSystem.Data
{
    public class WorkshopDbContext : DbContext
    {
        public WorkshopDbContext(DbContextOptions<WorkshopDbContext> options) : base(options)
        {
        }

        public DbSet<DiagnosticData> DiagnosticData { get; set; }

        public DbSet<RepairsData> RepairsData { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<DiagnosticData>()
                .HasKey(e => e.Id);

            modelBuilder.Entity<RepairsData>()
                .HasKey(e => e.Id);

            modelBuilder.Entity<RepairsData>()
                .Property(e => e.Status)
                .HasConversion<string>();


        }
    }
}
