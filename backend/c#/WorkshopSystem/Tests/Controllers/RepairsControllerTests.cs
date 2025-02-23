using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WorkshopSystem.Controllers;
using WorkshopSystem.Data;
using WorkshopSystem.Models;
using WorkshopSystem.Exceptions;
using Xunit;

namespace WorkshopSystem.Tests.Controllers
{
    public class RepairsControllerTests
    {
        private WorkshopDbContext GetDbContext()
        {
            var options = new DbContextOptionsBuilder<WorkshopDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;
            return new WorkshopDbContext(options);
        }

        [Fact]
        public async Task GetRepairs_ReturnsAllRepairs()
        {
            // Arrange
            using var context = GetDbContext();
            var controller = new RepairsController(context);
            var repair1 = new RepairsData
            {
                Description = "Test Repair 1",
                Status = RepairStatus.Pending,
                Mechanic = "John Doe",
                Notes = "Test notes",
                VehicleVin = "1HGCM82633A123456"
            };
            var repair2 = new RepairsData
            {
                Description = "Test Repair 2",
                Status = RepairStatus.InProgress,
                Mechanic = "Jane Smith",
                Notes = "Test notes 2",
                VehicleVin = "1HGCM82633A789012"
            };
            context.RepairsData.AddRange(repair1, repair2);
            await context.SaveChangesAsync();

            // Act
            var result = await controller.GetRepairs();

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var repairs = Assert.IsType<List<RepairsData>>(okResult.Value);
            Assert.Equal(2, repairs.Count);
        }

        [Fact]
        public async Task GetRepairDetails_ReturnsRepair_WhenRepairExists()
        {
            // Arrange
            using var context = GetDbContext();
            var controller = new RepairsController(context);
            var repair = new RepairsData
            {
                Description = "Test Repair",
                Status = RepairStatus.Pending,
                Mechanic = "John Doe",
                Notes = "Test notes",
                VehicleVin = "1HGCM82633A123456"
            };
            context.RepairsData.Add(repair);
            await context.SaveChangesAsync();

            // Act
            var result = await controller.GetRepairDetails(repair.Id);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedRepair = Assert.IsType<RepairsData>(okResult.Value);
            Assert.Equal(repair.Description, returnedRepair.Description);
        }

        [Fact]
        public async Task GetRepairDetails_ThrowsException_WhenRepairNotFound()
        {
            // Arrange
            using var context = GetDbContext();
            var controller = new RepairsController(context);

            // Act & Assert
            await Assert.ThrowsAsync<RepairsNotFoundException>(() =>
                controller.GetRepairDetails(999));
        }

        [Fact]
        public async Task AddRepair_CreatesNewRepair_WhenModelIsValid()
        {
            // Arrange
            using var context = GetDbContext();
            var controller = new RepairsController(context);
            var newRepair = new RepairsData
            {
                Id = 1,
                VehicleVin = "1HGCM82633A123456",
                Description = "New Repair",
                Status = RepairStatus.Pending,
                Mechanic = "John Doe",
                Notes = "Test notes",

            };

            // Act
            var result = await controller.AddRepair(newRepair);

            // Assert
            var createdResult = Assert.IsType<CreatedAtActionResult>(result);
            var returnedRepair = Assert.IsType<RepairsData>(createdResult.Value);
            Assert.Equal(newRepair.Description, returnedRepair.Description);
            Assert.Equal(1, await context.RepairsData.CountAsync());
        }

        [Fact]
        public async Task UpdateRepairStatus_UpdatesStatus_WhenRepairExists()
        {
            // Arrange
            using var context = GetDbContext();
            var controller = new RepairsController(context);
            var repair = new RepairsData
            {
                Description = "Test Repair",
                Status = RepairStatus.Pending,
                Mechanic = "John Doe",
                Notes = "Test notes",
                VehicleVin = "1HGCM82633A123456"
            };
            context.RepairsData.Add(repair);
            await context.SaveChangesAsync();

            // Act
            var result = await controller.UpdateRepairStatus(repair.Id, RepairStatus.Completed.ToString());

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var updatedRepair = Assert.IsType<RepairsData>(okResult.Value);
            Assert.Equal(RepairStatus.Completed, updatedRepair.Status);
        }

        [Fact]
        public async Task UpdateRepairStatus_ThrowsException_WhenRepairNotFound()
        {
            // Arrange
            using var context = GetDbContext();
            var controller = new RepairsController(context);

            // Act & Assert
            await Assert.ThrowsAsync<RepairsNotFoundException>(() =>
                controller.UpdateRepairStatus(999, RepairStatus.Completed.ToString()));
        }
    }
}
