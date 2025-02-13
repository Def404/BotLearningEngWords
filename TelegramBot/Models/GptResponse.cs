using System.Text.Json.Serialization;

namespace TelegramBot.Models
{
    public class GptResponse
    {
        [JsonPropertyName("result")]
        public Result Result { get; set; } = new Result();
    }

    public class Result
    {
        [JsonPropertyName("alternatives")]
        public Alternative[] Alternatives { get; set; } = Array.Empty<Alternative>();

        [JsonPropertyName("usage")]
        public Usage Usage { get; set; } = new Usage();

        [JsonPropertyName("modelVersion")]
        public string ModelVersion { get; set; } = string.Empty;
    }

    public class Alternative
    {
        [JsonPropertyName("message")]
        public GptMessage Message { get; set; } = new GptMessage();

        [JsonPropertyName("status")]
        public string Status { get; set; } = string.Empty;
    }

    public class Usage
    {
        [JsonPropertyName("inputTextTokens")]
        public string InputTextTokens { get; set; } = string.Empty;

        [JsonPropertyName("completionTokens")]
        public string CompletionTokens { get; set; } = string.Empty;

        [JsonPropertyName("totalTokens")]
        public string TotalTokens { get; set; } = string.Empty;
    }

}
