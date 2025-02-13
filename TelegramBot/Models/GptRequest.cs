using System.Text.Json.Serialization;

namespace TelegramBot.Models
{
    public class GptRequest
    {
        [JsonPropertyName("modelUri")]
        public string ModelUri { get; set; } = string.Empty;

        [JsonPropertyName("completionOptions")]
        public CompletionOptions CompletionOptions { get; set; } = new CompletionOptions();

        [JsonPropertyName("messages")]
        public GptMessage[] Messages { get; set; } = Array.Empty<GptMessage>();
    }

    public class CompletionOptions
    {
        [JsonPropertyName("stream")]
        public bool Stream { get; set; }

        [JsonPropertyName("temperature")]
        public double Temperature { get; set; }

        [JsonPropertyName("maxTokens")]
        public string MaxTokens { get; set; } = string.Empty;

        [JsonPropertyName("reasoningOptions")]
        public ReasoningOptions ReasoningOptions { get; set; } = new ReasoningOptions();
    }

    public class ReasoningOptions
    {
        [JsonPropertyName("mode")]
        public string Mode { get; set; } = string.Empty;
    }
}
