using Microsoft.Extensions.Configuration;

var configuration = new ConfigurationBuilder()
    .AddUserSecrets<Program>()
    .Build();

var token = configuration["Token"];

Console.WriteLine("Hello, World!");
