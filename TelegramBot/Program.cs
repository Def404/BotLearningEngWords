using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using NLog.Extensions.Logging;
using Telegram.Bot.Polling;
using Telegram.Bot.Types.Enums;
using Telegram.Bot;
using TelegramBot.Handlers;

var configuration = new ConfigurationBuilder()
    .AddUserSecrets<Program>()
    .Build();

var logger = LoggerFactory.Create(builder => builder.AddNLog()).CreateLogger<Program>();

var token = configuration["Token"];

if (token == null)
{
    logger.LogError("Token not found!");
    return;
}

var bot = new TelegramBotClient(token);

var receiverOptions = new ReceiverOptions
{
    AllowedUpdates = new[]
    {
        UpdateType.Message,
        UpdateType.CallbackQuery
    },
    ThrowPendingUpdates = true
};
using var cts = new CancellationTokenSource();

bot.StartReceiving(UpdateHandler.Invoke, ErrorHandler.Invoke, receiverOptions, cts.Token);

await bot.GetMeAsync();

logger.LogInformation("Bot started");

await Task.Delay(-1);