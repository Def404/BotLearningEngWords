using System.Text;
using Telegram.Bot;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;

namespace TelegramBot.Commands;

public class TranslateCmd : ICommand
{
    public string Name => "Translate";
    public string? Description => "Перевод текста RUS => ENG || ENG => RUS";
    public string CommandTag => "/translate";
    public string CommandInfo => "/translate [текст]";
    public int ParameterCount => 1;

    public async void Action(ITelegramBotClient botClient, Message message)
    {
        var folderId = "";
        var iamToken =
            "";

        if (message.Text is null)
            return;

        var chat = message.Chat;

        var parameter = CommandService.GetParameterForTranslate(message.Text, this.CommandTag);

        if (string.IsNullOrEmpty(parameter))
        {
            var errorText = $"Команла введена не правильно:\n\n`{this.CommandInfo}`";

            await botClient.SendTextMessageAsync(chat.Id, errorText,
                parseMode: ParseMode.Markdown,
                protectContent: true);

            return;
        }

        HttpClient client = new HttpClient();
        client.DefaultRequestHeaders.Add("Authorization", $"Bearer {iamToken}");

        var body =
            $"{{\n\"targetLanguageCode\": 'ru',\n\"texts\": [\"Hello\", \"World\"],\n\"folderId\": '{folderId}',\n}}";

        var content = new StringContent(body, Encoding.UTF8, "application/json");

        var response = await client.PostAsync("https://translate.api.cloud.yandex.net/translate/v2/translate", content);

        var jsonResponse = await response.Content.ReadAsStringAsync();

        await botClient.SendTextMessageAsync(chat.Id, jsonResponse,
            replyToMessageId: message.MessageId);
    }
}