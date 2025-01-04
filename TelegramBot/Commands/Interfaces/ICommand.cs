using Telegram.Bot;
using Telegram.Bot.Types;

namespace TelegramBot.Commands.Interfaces;

public interface ICommand
{
    string Name { get; }
    string? Description { get; }
    string CommandTag { get; }
    string CommandInfo { get; }
    int ParameterCount { get; }

    public void Action(ITelegramBotClient botClient, Message message);
}