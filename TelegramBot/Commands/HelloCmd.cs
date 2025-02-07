using Telegram.Bot;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;
using TelegramBot.Commands.Helpers;
using TelegramBot.Commands.Interfaces;

namespace TelegramBot.Commands;

public class HelloCmd : ICommand
{
    public string Name => "Hello";
    public string Description => "Комманда отправляет привет пользователю";
    public string CommandTag => "/hi";
    public string CommandInfo => "/hi";
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

        await botClient.SendMessage(chat.Id, $"Привет, {user.FirstName}!",
            replyParameters: message.MessageId);
    }
}