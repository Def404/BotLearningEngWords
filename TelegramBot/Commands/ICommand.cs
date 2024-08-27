using Telegram.Bot;
using Telegram.Bot.Types;

namespace TelegramBot.Commands;

public interface ICommand
{
    string Name { get; }
    string? Description { get; }
    string Command { get; }
    int ParameterCount { get; }

    public void Action(ITelegramBotClient botClient, Message message);
}