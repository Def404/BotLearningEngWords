using Telegram.Bot;
using Telegram.Bot.Types;
using static System.Net.Mime.MediaTypeNames;
using Telegram.Bot.Types.Enums;

namespace TelegramBot.Commands;

public class HelloCmd : ICommand
{
    public string Name => "Hello";
    public string? Description => "Комманда отправляет привет пользователю";
    public string CommandTag => "/hi";
    public string CommandInfo => "/hi";
    public int ParameterCount => 0;

    public async void Action(ITelegramBotClient botClient, Message message)
    {
        var user = message.From;
        var chat = message.Chat;

        if (message.Text is null)
            return;

        var parameters = CommandService.GetParameters(message.Text, this.CommandTag);

        if(!(parameters.Length == this.ParameterCount))
        {
            var errorText = $"Команла введена не правильно:\n\n`{this.CommandInfo}`";

            await botClient.SendTextMessageAsync(chat.Id, errorText,
            parseMode: ParseMode.Markdown,
            protectContent: true);
        }

        await botClient.SendTextMessageAsync(chat.Id, $"Привет, {user.FirstName}!",
            replyToMessageId: message.MessageId);
    }
}