FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY src/ .
COPY dashboards-inventario/ ./dashboards-inventario/
RUN dotnet publish -c Release -o out
ENTRYPOINT ["dotnet", "out/InventarioAPI.dll"]