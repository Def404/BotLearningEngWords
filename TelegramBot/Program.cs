using DatabaseClassLibrary.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
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
            .AddDbContext<DatabaseContext>(options =>
                options.UseNpgsql(connectionString))
            .CommandInit()
            .AddTransient<UserServices>()
            .BuildServiceProvider();

        var token = Environment.GetEnvironmentVariable("TELEGRAM_BOT_TOKEN") ?? "";

        using var cts = new CancellationTokenSource();
        var bot = new TelegramBotClient(token, cancellationToken: cts.Token);

        var me = await bot.GetMe();
        await bot.DeleteWebhook();
        await bot.DropPendingUpdates();

        TelegramHandlers telegramHandlers = new TelegramHandlers(cts, bot, me, serviceProvider);

        bot.OnError += telegramHandlers.OnError;
        bot.OnMessage += telegramHandlers.OnMessage;
        bot.OnUpdate += telegramHandlers.OnUpdate;

        Console.WriteLine($"@{me.Username} is running... Press Escape to terminate");
        while (Console.ReadKey(true).Key != ConsoleKey.Escape) ;
        cts.Cancel();
    }
}