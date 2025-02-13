using Telegram.Bot;
using Telegram.Bot.Types;
using TelegramBot.Commands.Interfaces;
using TelegramBot.Services;

namespace TelegramBot.Commands
{
    public class DeleteUserCmd : ICommand
    {
        private readonly UserServices userServices;

        public DeleteUserCmd(UserServices services)
        {
            userServices = services;
        }

        public string Name => "DeleteUser";
        public string Description => "Команда удаления пользователя";
        public string CommandTag => "/deleteUser";
        public string CommandInfo => "/deleteUser";
        public int ParameterCount => 0;

        public async Task Action(ITelegramBotClient botClient, Message message)
        {
            var user = message.From;

            if (user == null)
                return;

            var chat = message.Chat;

            if (message.Text is null)
                return;

            var result = await userServices.DeleteUserAsync(user);

            if (result)
            {
                await botClient.SendMessage(chat.Id, $"Вы успешно удалены из системы!");
            }
            else
            {
                await botClient.SendMessage(chat.Id, $"Вы не зарегистрированы в системе!");
            }

        }
    }
}
