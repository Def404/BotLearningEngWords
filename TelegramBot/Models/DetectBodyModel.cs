using System.Text.Json.Serialization;

namespace TelegramBot.Models;

public class DetectBodyModel
{
    [JsonPropertyName("folderId")]
    public string FolderId {get; set;} = string.Empty;

    [JsonPropertyName("languageCodeHints")]
    public string[] LanguageCodeHints {get; set;} = Array.Empty<string>();

    [JsonPropertyName("text")]
    public string Text { get; set; } = string.Empty;
}