using DatabaseClassLibrary.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using NLog.Extensions.Logging;
using Telegram.Bot;
using TelegramBot.Extensions;
using TelegramBot.Handlers;
using TelegramBot.Services;

internal class Program
{
    private static async Task Main(string[] args)
    {
        var connectionString = Environment.GetEnvironmentVariable("DATABASE_CONNECTION_STRING") ?? "";

        var serviceProvider = new ServiceCollection()
            .AddLogging(loggingBuilder =>
            {
                loggingBuilder.ClearProviders();
                loggingBuilder.SetMinimumLevel(LogLevel.Trace);
                loggingBuilder.AddNLog();
            })
            .AddDbContext<DatabaseContext>(options =>
                options.UseNpgsql(connectionString))
            .CommandInit()
            .AddTransient<UserServices>()
            .BuildServiceProvider();

        using (var scope = serviceProvider.CreateScope())
        {
            var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
            var userService = scope.ServiceProvider.GetRequiredService<UserServices>();

            try
            {
                var token = Environment.GetEnvironmentVariable("TELEGRAM_BOT_TOKEN") ?? "";

                if (string.IsNullOrEmpty(token))
                {
                    logger.LogError("No token provided");
                    return;
                }

                using var cts = new CancellationTokenSource();
                var bot = new TelegramBotClient(token, cancellationToken: cts.Token);

                var me = await bot.GetMe();
                await bot.DeleteWebhook();
                await bot.DropPendingUpdates();

                TelegramHandlers telegramHandlers = new TelegramHandlers(cts, bot, me, serviceProvider);

                bot.OnError += telegramHandlers.OnError;
                bot.OnMessage += telegramHandlers.OnMessage;
                bot.OnUpdate += telegramHandlers.OnUpdate;

                logger.LogInformation($"@{me.Username} is running... Press Escape to terminate");
                while (Console.ReadKey(true).Key != ConsoleKey.Escape) ;
                cts.Cancel();
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Error app");
            }

            logger.LogInformation("Stop app");
        }

        NLog.LogManager.Shutdown();
    }
}