using System.Text.Json.Serialization;

namespace TelegramBot.Models
{
    public class GptMessage
    {
        [JsonPropertyName("role")]
        public string Role { get; set; } = string.Empty;

        [JsonPropertyName("text")]
        public string Text { get; set; } = string.Empty;
    }
}
