using Microsoft.Extensions.Logging;
using Telegram.Bot;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;
using TelegramBot.Commands.Helpers;
using TelegramBot.Commands.Interfaces;
using TelegramBot.Services;

namespace TelegramBot.Commands;

public class TranslateCmd : ICommand
{
    private readonly YandexApiService _yandexApiService;

    public TranslateCmd(ILogger<TranslateCmd> logger, YandexApiService yandexApiService)
    {
        _yandexApiService = yandexApiService;
    }

    public string Name => "Translate";
    public string? Description => "Перевод текста RUS => ENG || ENG => RUS";
    public string CommandTag => "/translate";
    public string CommandInfo => "/translate [текст]";
    public int ParameterCount => 1;

    public async Task Action(ITelegramBotClient botClient, Message message)
    {
        if (message.Text is null)
            return;

        var chat = message.Chat;

        var parameter = CommandHelpers.GetParameterForTranslate(message.Text, this.CommandTag);

        if (string.IsNullOrEmpty(parameter))
        {
            var errorText = $"Команда введена не правильно:\n\n`{this.CommandInfo}`";

            await botClient.SendMessage(chat.Id, errorText,
                parseMode: ParseMode.Markdown,
                protectContent: true);

            return;
        }

        var detectLanguage = await _yandexApiService.DetectLanguageAsync(parameter);

        var targetLanguageCode = "";

        switch (detectLanguage)
        {
            case "ru":
                targetLanguageCode = "en";
                break;
            case "en":
                targetLanguageCode = "ru";
                break;
            default:
                {
                    var errorText = $"Вы ввели неподдерживаемый язык";

                    await botClient.SendMessage(chat.Id, errorText,
                        parseMode: ParseMode.Markdown,
                        protectContent: true);

                    return;
                }
        }

        var translateMessage = await _yandexApiService.TranslateAsync(parameter, targetLanguageCode);

        if (string.IsNullOrEmpty(translateMessage))
        {
            var errorText = $"Не удалось перевести текст";

            await botClient.SendMessage(chat.Id, errorText,
                parseMode: ParseMode.Markdown,
                protectContent: true);

            return;
        }

        await botClient.SendMessage(chat.Id, translateMessage,
            replyParameters: message.MessageId);
    }
}