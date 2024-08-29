using Telegram.Bot;
using Telegram.Bot.Types;

namespace TelegramBot.Handlers;

public abstract class UpdateHandler : Handler
{
    public static async Task Invoke(ITelegramBotClient botClient, Update update,
        CancellationToken cancellationToken)
    {
        if (update.Message is null) return;
        if (update.Message.Text is null) return;

        var massage = update.Message;

        var cmd = massage.Text.Split(' ');

        foreach (var command in CommandsList.Commands.Where(command => cmd[0].Equals(command.CommandTag)))
        {
            command.Action(botClient, update.Message);
        }

        /*if (massage != null)
        {
            var user = massage.From;
            var chat = massage.Chat;

            await botClient.SendTextMessageAsync(chat.Id, massage.Text);
        }*/
    }
}