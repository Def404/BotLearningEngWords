using System.Text.Json.Serialization;

namespace TelegramBot.Models;

public class DetectLangResponse
{
    [JsonPropertyName("languageCode")]
    public string LanguageCode { get; set; } = string.Empty;
}