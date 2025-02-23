using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WorkshopSystem.Data;
using WorkshopSystem.Models;
using WorkshopSystem.Exceptions;

namespace WorkshopSystem.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DiagnosticsController : ControllerBase
    {
        private readonly WorkshopDbContext _context;

        public DiagnosticsController(WorkshopDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetDiagnosticData()
        {
            try
            {
                var diagnosticData = await _context.DiagnosticData.ToListAsync();
                return Ok(diagnosticData);
            }
            catch (DiagnosticException ex)
            {
                throw new DiagnosticException("Error fetching diagnostic data", ex);
            }


        }

        [HttpPost]
        public async Task<IActionResult> AddDiagnostic([FromBody] DiagnosticData data)
        {

            try
            {
                _context.DiagnosticData.Add(data);
                await _context.SaveChangesAsync();
                return CreatedAtAction(nameof(GetDiagnosticData), new { id = data.Id }, data);
            }
            catch (DiagnosticException ex)
            {
                throw new DiagnosticException("Error adding diagnostic data", ex);
            }


        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteDiagnostic(int id)
        {
            try
            {
                var diagnostic = await _context.DiagnosticData.FindAsync(id);

                if (diagnostic == null)
                {
                    throw new DiagnosticNotFoundException("Diagnostic not found");
                }

                _context.DiagnosticData.Remove(diagnostic);
                await _context.SaveChangesAsync();
                return NoContent();
            }
            catch (DiagnosticException ex)
            {
                throw new DiagnosticException("Error deleting diagnostic data", ex);
            }
        }
    }
}