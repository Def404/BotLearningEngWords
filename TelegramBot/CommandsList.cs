using TelegramBot.Commands;
using TelegramBot.Commands.Interfaces;

namespace TelegramBot;

public class CommandsList
{
    public static readonly List<ICommand> Commands = [new HelpCmd(), new HelloCmd(), new TranslateCmd()];
}