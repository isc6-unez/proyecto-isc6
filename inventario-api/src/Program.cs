using Microsoft.EntityFrameworkCore;
// Importa el espacio de nombres donde se encuentre tu DbContext, ej:
using InventarioAPI.Data; 

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://+:5000");

// 1. Obtener la cadena de conexión
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// 2. Registrar DbContext con PostgreSQL
builder.Services.AddDbContext<InventarioDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();