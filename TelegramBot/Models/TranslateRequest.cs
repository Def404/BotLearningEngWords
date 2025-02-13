using System.Text.Json.Serialization;

namespace TelegramBot.Models;

public class TranslateRequest
{
    [JsonPropertyName("targetLanguageCode")]
    public string TargetLanguageCode {get; set;} = string.Empty;

    [JsonPropertyName("texts")]
    public string[] Texts {get; set;} = Array.Empty<string>();

    [JsonPropertyName("folderId")]
    public string FolderId { get; set; } = string.Empty;

}