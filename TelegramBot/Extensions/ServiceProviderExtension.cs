using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TelegramBot.Commands;
using TelegramBot.Commands.Interfaces;
using TelegramBot.Options;

namespace TelegramBot.Extensions
{
    public static class ServiceProviderExtension
    {
        public static IServiceCollection AddCommandHandlers(this IServiceCollection services)
        {
            services.AddSingleton<ICommand, HelpCmd>();
            services.AddSingleton<ICommand, HelloCmd>();
            services.AddSingleton<ICommand, TranslateCmd>();
            services.AddSingleton<ICommand, StartCmd>();
            services.AddSingleton<ICommand, DeleteUserCmd>();

            return services;
        }

        public static IServiceCollection ConfigureAppSettings(this IServiceCollection services, IConfiguration config)
        {
            services.Configure<BotConfig>(config.GetSection("Bot"));
            services.Configure<YandexConfig>(config.GetSection("Yandex"));
            services.Configure<DBConfig>(config.GetSection("DB"));
            services.Configure<PromptConfig>(config.GetSection("Prompt"));

            return services;
        }
    }
}
