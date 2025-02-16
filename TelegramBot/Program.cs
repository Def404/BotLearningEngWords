using DatabaseClassLibrary.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using NLog.Extensions.Logging;
using Telegram.Bot;
using TelegramBot.Extensions;
using TelegramBot.Handlers;
using TelegramBot.Options;
using TelegramBot.Services;

internal class Program
{
    public static async Task Main(string[] args)
    {
        var host = CreateHostBuilder(args).Build();

        using (var scope = host.Services.CreateScope())
        {
            var services = scope.ServiceProvider;
            var logger = services.GetRequiredService<ILogger<Program>>();

            try
            {
                await RunBotAsync(services, logger);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Fatal error occurred");
            }
        }

        await host.StopAsync();
        NLog.LogManager.Shutdown();
    }

    private static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureAppConfiguration((hostingContext, config) =>
            {
                config.AddEnvironmentVariables();
            })
            .ConfigureLogging(logging =>
            {
                logging.ClearProviders();
                logging.SetMinimumLevel(LogLevel.Trace);
                logging.AddNLog();
            })
            .ConfigureServices((hostContext, services) =>
            {
                var config = hostContext.Configuration;

                services
                    .ConfigureAppSettings(config)
                    .AddDbContext<DatabaseContext>(options =>
                        options.UseNpgsql(config.GetSection("DB")["ConnectionString"] ?? ""))
                    .AddCommandHandlers()
                    .AddTransient<UserServices>()
                    .AddHttpClient()
                    .AddHttpClient<YandexApiService>((provider, client) =>
                    {
                        var yandexConfig = provider.GetRequiredService<IOptions<YandexConfig>>().Value;
                        client.DefaultRequestHeaders.Add("Authorization", $"Api-Key {yandexConfig.ApiToken}");
                        client.DefaultRequestHeaders.Add("x-folder-id", yandexConfig.FolderId ?? "");
                    });
            });

    private static async Task RunBotAsync(IServiceProvider services, ILogger logger)
    {
        using var scope = services.CreateScope();
        var botConfig = scope.ServiceProvider.GetRequiredService<IOptions<BotConfig>>().Value;

        if (string.IsNullOrEmpty(botConfig.Token))
        {
            logger.LogError("No token provided");
            return;
        }

        using var cts = new CancellationTokenSource();
        var bot = new TelegramBotClient(botConfig.Token, cancellationToken: cts.Token);
        var me = await bot.GetMe();

        await bot.DeleteWebhook();
        await bot.DropPendingUpdates();

        var telegramHandlers = new TelegramHandlers(cts, bot, me, services);
        bot.OnError += telegramHandlers.OnError;
        bot.OnMessage += telegramHandlers.OnMessage;
        bot.OnUpdate += telegramHandlers.OnUpdate;

        logger.LogInformation($"@{me.Username} is running...");

        await SendStartupMessages(services, bot);

        await Task.Delay(Timeout.Infinite, cts.Token);
    }

    private static async Task SendStartupMessages(IServiceProvider services, TelegramBotClient bot)
    {
        using var scope = services.CreateScope();
        var promptConfig = scope.ServiceProvider.GetRequiredService<IOptions<PromptConfig>>().Value;
        var botConfig = scope.ServiceProvider.GetRequiredService<IOptions<BotConfig>>().Value;
        var userServices = scope.ServiceProvider.GetRequiredService<UserServices>();
        var yandexApiService = scope.ServiceProvider.GetRequiredService<YandexApiService>();

        if (!botConfig.SendStartupMessage) return;

        var users = await userServices.GetAllUsersAsync();
        var startMessage = promptConfig.StartMessage ?? "Ура! Я готов к работе!";

        await Task.WhenAll(users.Select(async user =>
            bot.SendMessage(user.telegram_user_id, await yandexApiService.GenerateGtpMassageAsync(startMessage))));
    }
}
