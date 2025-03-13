using Xunit;
using Moq;
using Microsoft.EntityFrameworkCore;
using WorkshopSystem.Controllers;
using WorkshopSystem.Data;
using WorkshopSystem.Models;
using WorkshopSystem.Exceptions;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Linq;
using System;

public class DiagnosticsControllerTests
{
    private WorkshopDbContext GetInMemoryDbContext()
    {
        var dbName = $"TestDatabase_{Guid.NewGuid()}";

        var options = new DbContextOptionsBuilder<WorkshopDbContext>()
            .UseInMemoryDatabase(databaseName: dbName)
            .Options;

        var context = new WorkshopDbContext(options);

        context.DiagnosticData.Add(new DiagnosticData { Id = 1, VehicleVin = "VIN123", Description = "Check Engine Light", Mechanic = "John Doe" });
        context.DiagnosticData.Add(new DiagnosticData { Id = 2, VehicleVin = "VIN456", Description = "Brake Inspection", Mechanic = "Jane Doe" });
        context.SaveChanges();

        return context;
    }

    [Fact]
    public async Task GetDiagnosticData_ReturnsAllDiagnostics()
    {
        // Arrange
        var context = GetInMemoryDbContext();
        var controller = new DiagnosticsController(context);

        // Act
        var result = await controller.GetDiagnosticData();

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result);
        var diagnostics = Assert.IsType<List<DiagnosticData>>(okResult.Value);
        Assert.Equal(2, diagnostics.Count);
    }

    [Fact]
    public async Task AddDiagnostic_ReturnsCreatedAtAction()
    {
        // Arrange
        var context = GetInMemoryDbContext();
        var controller = new DiagnosticsController(context);
        var newDiagnostic = new DiagnosticData { Id = 3, VehicleVin = "VIN789", Description = "Oil Change", Mechanic = "Mike Doe" };

        // Act
        var result = await controller.AddDiagnostic(newDiagnostic);

        // Assert
        var createdResult = Assert.IsType<CreatedAtActionResult>(result);
        var diagnostic = Assert.IsType<DiagnosticData>(createdResult.Value);
        Assert.Equal("VIN789", diagnostic.VehicleVin);
    }

    [Fact]
    public async Task DeleteDiagnostic_ReturnsNoContent_WhenDiagnosticExists()
    {
        // Arrange
        var context = GetInMemoryDbContext();
        var controller = new DiagnosticsController(context);

        // Act
        var result = await controller.DeleteDiagnostic(1);

        // Assert
        Assert.IsType<NoContentResult>(result);
        Assert.Null(await context.DiagnosticData.FindAsync(1));
    }

    [Fact]
    public async Task DeleteDiagnostic_ReturnsNotFound_WhenDiagnosticDoesNotExist()
    {
        // Arrange
        var context = GetInMemoryDbContext();
        var controller = new DiagnosticsController(context);

        // Act
        var exception = await Assert.ThrowsAsync<DiagnosticNotFoundException>(async () =>
            await controller.DeleteDiagnostic(999));

        // Assert
        Assert.Equal("Diagnostic not found", exception.Message);
    }


}
