using System.Text.Json.Serialization;

namespace TelegramBot.Models;

public class TranslateResponse
{
    [JsonPropertyName("translations")]
    public List<Translation> Translations { get; set; } = new List<Translation>();

    public class Translation
    {
        [JsonPropertyName("text")]
        public string Text { get; set; } = string.Empty;

        [JsonPropertyName("detectedLanguageCode")]
        public string DetectedLanguageCode { get; set; } = string.Empty;
    }

}