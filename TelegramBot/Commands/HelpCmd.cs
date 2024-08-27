using Telegram.Bot;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;

namespace TelegramBot.Commands;

public class HelpCmd : ICommand
{
    public string Name => "Help";
    public string? Description => "Помощь";
    public string Command => "/help";
    public int ParameterCount => 0;

    public async void Action(ITelegramBotClient botClient, Update update)
    {
        var massage = update.Message;

        if (massage is null) return;

        var chat = massage.Chat;

        var text = "Данный бот позволит Вам изучить английские слова! \n\n" +
                   "Вы сможете хранить все изученые слова в одном месте\n" +
                   "Пройти тест на знание изученных слов\n" +
                   "Переводить слова и фразы\n\n" +
                   "*Команды:*\n" +
                   "`";

        foreach (var command in CommandsList.Commands)
        {
            text += $"{command.Command} - {command.Description}\n";
        }

        text += "`\n\n" +
                "Разработчик: @adef15";

        await botClient.SendTextMessageAsync(chat.Id, text,
            parseMode: ParseMode.Markdown,
            protectContent: true);
    }
}