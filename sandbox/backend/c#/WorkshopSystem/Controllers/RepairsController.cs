using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WorkshopSystem.Data;
using WorkshopSystem.Models;
using WorkshopSystem.Exceptions;
namespace WorkshopSystem.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RepairsController : ControllerBase
    {
        private readonly WorkshopDbContext _context;

        public RepairsController(WorkshopDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetRepairs()
        {
            var repairs = await _context.RepairsData.ToListAsync();
            return Ok(repairs);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetRepairDetails(int id)
        {
            var repair = await _context.RepairsData.FindAsync(id);

            if (repair == null)
            {
                throw new RepairsNotFoundException($"Repair with ID {id} not found");
            }

            return Ok(repair);
        }

        [HttpPost]
        public async Task<IActionResult> AddRepair([FromBody] RepairsData repair)
        {
            if (repair == null)
            {
                return BadRequest("Repair data cannot be null");
            }

            _context.RepairsData.Add(repair);
            await _context.SaveChangesAsync();
            return CreatedAtAction(nameof(GetRepairs), new { id = repair.Id }, repair);
        }

        [HttpPut("{id}/status")]
        public async Task<IActionResult> UpdateRepairStatus(int id, [FromBody] string newStatus)
        {
            var repair = await _context.RepairsData.FindAsync(id);

            if (repair == null)
            {
                throw new RepairsNotFoundException($"Repair with ID {id} not found");
            }

            repair.Status = Enum.Parse<RepairStatus>(newStatus);
            await _context.SaveChangesAsync();

            return Ok(repair);
        }
    }
}