FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY src/ .
RUN dotnet publish -c Release -o out
ENTRYPOINT ["dotnet", "out/InventarioAPI.dll"]
