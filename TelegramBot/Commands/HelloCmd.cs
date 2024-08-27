using Telegram.Bot;
using Telegram.Bot.Types;

namespace TelegramBot.Commands;

public class HelloCmd : ICommand
{
    public string Name => "Hello";
    public string? Description => "Комманда отправляет привет пользователю";

    public string Command => "/hi";
    /*public string[]? ParameterKeys => null;
    public int ParameterCount => 0;*/

    public async void Action(ITelegramBotClient botClient, Update update)
    {
        var massage = update.Message;
        var user = massage.From;
        var chat = massage.Chat;

        await botClient.SendTextMessageAsync(chat.Id, $"Привет, {user.FirstName}!",
            replyToMessageId: update.Message.MessageId);
    }
}