using Newtonsoft.Json;
using System.Text;
using Telegram.Bot;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;
using TelegramBot.Commands.Helpers;
using TelegramBot.Commands.Interfaces;
using TelegramBot.Models;

namespace TelegramBot.Commands;

public class TranslateCmd : ICommand
{
    public string Name => "Translate";
    public string? Description => "Перевод текста RUS => ENG || ENG => RUS";
    public string CommandTag => "/translate";
    public string CommandInfo => "/translate [текст]";
    public int ParameterCount => 1;

    public async Task Action(ITelegramBotClient botClient, Message message)
    {
        var folderId = Environment.GetEnvironmentVariable("FOLDER_ID") ?? "";
        var iamToken = Environment.GetEnvironmentVariable("IAM_TOKEN") ?? "";

        if (String.IsNullOrEmpty(folderId) || String.IsNullOrEmpty(iamToken))
        {
            Console.WriteLine("No folder id or iam token provided");
            return;
        }

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

        var client = new HttpClient();
        client.DefaultRequestHeaders.Add("Authorization", $"Bearer {iamToken}");

        var languageCodeHints = new string[] { "ru", "en" };
        var detectBodyModel = new DetectBodyModel(folderId, languageCodeHints, parameter);

        var detectBodyJson = JsonConvert.SerializeObject(detectBodyModel);

        var detectContent = new StringContent(detectBodyJson, Encoding.UTF8, "application/json");
        var detectResponse = await client.PostAsync("https://translate.api.cloud.yandex.net/translate/v2/detect", detectContent);

        if (detectResponse.StatusCode != System.Net.HttpStatusCode.OK)
        {
            return;
        }

        var detectJsonResponse = await detectResponse.Content.ReadAsStringAsync();

        var detectResponseModel = JsonConvert.DeserializeObject<DetectResponseModel>(detectJsonResponse);

        if (detectResponseModel == null)
        {
            var errorText = $"Не удалось определить язык введенного текста";

            await botClient.SendMessage(chat.Id, errorText,
                parseMode: ParseMode.Markdown,
                protectContent: true);

            return;
        }

        var targetLanguageCode = "";

        switch (detectResponseModel.languageCode)
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

        var translateBodyModel = new TranslateBodyModel(folderId, targetLanguageCode, parameter);
        var translateBodyJson = JsonConvert.SerializeObject(translateBodyModel);
        var translateContent = new StringContent(translateBodyJson, Encoding.UTF8, "application/json");

        var translateResponse = await client.PostAsync("https://translate.api.cloud.yandex.net/translate/v2/translate", translateContent);

        if (translateResponse.StatusCode != System.Net.HttpStatusCode.OK)
        {
            return;
        }

        var translateJsonResponse = await translateResponse.Content.ReadAsStringAsync();

        var translateResponseModel = JsonConvert.DeserializeObject<TranslateResponseModel>(translateJsonResponse);

        if (translateResponseModel == null)
        {
            var errorText = $"Не удалось перевести текст";

            await botClient.SendMessage(chat.Id, errorText,
                parseMode: ParseMode.Markdown,
                protectContent: true);

            return;
        }

        await botClient.SendMessage(chat.Id, translateResponseModel.translations.First().text,
            replyParameters: message.MessageId);
    }
}