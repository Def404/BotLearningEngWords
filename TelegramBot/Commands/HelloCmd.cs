using Telegram.Bot;
using Telegram.Bot.Types;

namespace TelegramBot.Commands;

public class HelloCmd : ICommand
{
    public string Name => "Hello";
    public string? Description => "Комманда отправляет привет пользователю";
    public string Command => "/hi";
    public int ParameterCount => 0;

    public async void Action(ITelegramBotClient botClient, Message message)
    {
        var user = message.From;
        var chat = message.Chat;

        await botClient.SendTextMessageAsync(chat.Id, $"Привет, {user.FirstName}!",
            replyToMessageId: message.MessageId);
    }
}