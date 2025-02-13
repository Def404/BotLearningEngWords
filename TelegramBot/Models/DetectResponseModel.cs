using System.Text.Json.Serialization;

namespace TelegramBot.Models;

public class DetectResponseModel
{
    [JsonPropertyName("languageCode")]
    public string LanguageCode { get; set; } = string.Empty;
}