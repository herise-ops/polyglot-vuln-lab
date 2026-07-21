# .NET 6 is intentionally out of support and should be reported by container scanners.
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY VulnerableApi.csproj ./
RUN dotnet restore
COPY Program.cs ./
RUN dotnet publish -c Release -o /out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:6.0
WORKDIR /app
COPY --from=build /out ./
ENV ASPNETCORE_URLS=http://0.0.0.0:8082
EXPOSE 8082
ENTRYPOINT ["dotnet", "VulnerableApi.dll"]
