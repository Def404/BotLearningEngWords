using Microsoft.Extensions.DependencyInjection;
using TelegramBot.Commands;
using TelegramBot.Commands.Interfaces;

namespace TelegramBot.Extensions
{
    public static class ServiceProviderExtension
    {
        public static IServiceCollection CommandInit(this IServiceCollection services)
        {
            services.AddSingleton<ICommand, HelpCmd>();
            services.AddSingleton<ICommand, HelloCmd>();
            services.AddSingleton<ICommand, TranslateCmd>();
            services.AddSingleton<ICommand, StartCmd>();
            services.AddSingleton<ICommand, DeleteUserCmd>();

            return services;
        }
    }
}
