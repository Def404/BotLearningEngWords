using TelegramBot.Commands;

namespace TelegramBot;

public static class CommandsList
{
    public static readonly List<ICommand> Commands = [new HelpCmd(), new HelloCmd()];
}