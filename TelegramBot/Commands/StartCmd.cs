using Telegram.Bot;
using Telegram.Bot.Types;
using TelegramBot.Commands.Helpers;
using TelegramBot.Commands.Interfaces;
using TelegramBot.Services;

namespace TelegramBot.Commands
{
    public class StartCmd : ICommand
    {
        private readonly UserServices userServices;

        public StartCmd(UserServices services)
        {
            userServices = services;
        }

        public string Name => "Start";
        public string Description => "Начальная команда";
        public string CommandTag => "/start";
        public string CommandInfo => "/start";
        public int ParameterCount => 0;

        public async Task Action(ITelegramBotClient botClient, Message message)
        {
            var user = message.From;

            if (user == null)
                return;

            var chat = message.Chat;

            if (message.Text is null)
                return;

            var parameters = CommandHelpers.GetParameters(message.Text, this.CommandTag);

            var result = await userServices.InitUser(user);

            if (result)
            {
                await botClient.SendMessage(chat.Id, $"Вы успешно зарегистрировались в системе!");
            }
            else
            {
                await botClient.SendMessage(chat.Id, $"Вы уже зарегистрированы в системе!");
            }

        }
    }
}
