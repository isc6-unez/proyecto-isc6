using Microsoft.EntityFrameworkCore;
using InventarioAPI.Data; 
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);

// Obligar a la API a iniciar en el puerto 5000 para mapeo con Docker
builder.WebHost.UseUrls("http://+:5000"); 

// 1. Obtener la cadena de conexión
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// 2. Registrar DbContext con PostgreSQL
builder.Services.AddDbContext<InventarioDbContext>(options =>
    options.UseNpgsql(connectionString));

// 3. Registrar Servicios
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 4. Configurar CORS (Permite peticiones desde el Dashboard)
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Configuración de archivos estáticos para dashboards-inventario
var dashboardsPath = Path.Combine(app.Environment.ContentRootPath, "dashboards-inventario");
if (Directory.Exists(dashboardsPath))
{
    app.UseStaticFiles(new StaticFileOptions
    {
        FileProvider = new PhysicalFileProvider(dashboardsPath),
        RequestPath = "/dashboards-inventario"
    });
}
app.UseStaticFiles();

// Habilitar Swagger siempre (Desarrollo y Producción/Docker)
app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();

// ⚠️ Importante: CORS debe activarse ANTES de mapear los controladores
app.UseCors();

app.UseAuthorization();
app.MapControllers();

app.Run();