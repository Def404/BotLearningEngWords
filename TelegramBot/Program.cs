using Microsoft.Extensions.Configuration;
using Telegram.Bot;
using TelegramBot.Handlers;

internal class Program
{
    private static async Task Main(string[] args)
    {
        var token = Environment.GetEnvironmentVariable("TELEGRAM_BOT_TOKEN") ?? "";

        using var cts = new CancellationTokenSource();
        var bot = new TelegramBotClient(token, cancellationToken: cts.Token);

        var me = await bot.GetMe();
        await bot.DeleteWebhook();
        await bot.DropPendingUpdates();

        TelegramHandlers telegramHandlers = new TelegramHandlers(cts, bot, me);

        bot.OnError += telegramHandlers.OnError;
        bot.OnMessage += telegramHandlers.OnMessage;
        bot.OnUpdate += telegramHandlers.OnUpdate;

        Console.WriteLine($"@{me.Username} is running... Press Escape to terminate");
        while (Console.ReadKey(true).Key != ConsoleKey.Escape) ;
        cts.Cancel();
    }
}