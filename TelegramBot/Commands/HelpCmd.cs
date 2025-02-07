using Microsoft.Extensions.DependencyInjection;
using Telegram.Bot;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;
using Telegram.Bot.Types.ReplyMarkups;
using TelegramBot.Commands.Helpers;
using TelegramBot.Commands.Interfaces;

namespace TelegramBot.Commands;

public class HelpCmd : ICommand
{
    private readonly IServiceProvider _serviceProvider;

    public HelpCmd(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public string Name => "Help";
    public string Description => "Помощь";
    public string CommandTag => "/help";
    public string CommandInfo => "/help";
    public int ParameterCount => 0;

    public async Task Action(ITelegramBotClient botClient, Message message)
    {
        if (message.Text is null)
            return;

        var chat = message.Chat;

        var parameters = CommandHelpers.GetParameters(message.Text, this.CommandTag);

        if (parameters.Length != this.ParameterCount)
        {
            var errorText = $"Команла введена не правильно:\n\n`{this.CommandInfo}`";

            await botClient.SendMessage(chat.Id, errorText,
                parseMode: ParseMode.Markdown,
                protectContent: true);

            return;
        }

        var newText = """
            Данный бот позволит Вам изучить английские слова!

            Вы сможете хранить все изученые слова в одном месте
            Пройти тест на знание изученных слов
            Переводить слова и фразы

            <b><u>Команды</u></b>:

            """;

        var commands = _serviceProvider.GetServices<ICommand>();
        foreach (var command in commands)
        {
            newText += $"{command.CommandTag} - {command.Description}\n";
        }

        newText += """

            Разработчик: @adef15
            """;

        await botClient.SendMessage(chat.Id, newText,
            parseMode: ParseMode.Html, linkPreviewOptions: true,
            replyMarkup: new ReplyKeyboardRemove());
    }
}