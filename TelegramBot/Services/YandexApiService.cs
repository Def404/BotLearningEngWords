using Microsoft.Extensions.Logging;
using System.Text.Json;
using System.Text;
using TelegramBot.Models;

namespace TelegramBot.Services
{
    public class YandexApiService
    {
        private readonly string FOLDER_ID = Environment.GetEnvironmentVariable("FOLDER_ID") ?? "";
        private readonly string IAM_TOKEN = Environment.GetEnvironmentVariable("IAM_TOKEN") ?? "";

        private readonly ILogger<YandexApiService> _logger;
        private readonly HttpClient _httpClient;

        public YandexApiService(ILogger<YandexApiService> logger, HttpClient httpClient)
        {
            _logger = logger;
            _httpClient = httpClient;
        }

        public async Task<string> GenerateGtpMassageAsync(string promt)
        {
            if (string.IsNullOrEmpty(FOLDER_ID) || string.IsNullOrEmpty(IAM_TOKEN))
            {
                _logger.LogError("No folder id or iam token provided");
                return string.Empty;
            }

            var requestModel = new GptRequest
            {
                ModelUri = $"gpt://{FOLDER_ID}/yandexgpt",
                CompletionOptions = new CompletionOptions
                {
                    Stream = false,
                    Temperature = 0.7,
                    MaxTokens = "2000",
                    ReasoningOptions = new ReasoningOptions
                    {
                        Mode = "DISABLED",
                    },
                },
                Messages = new GptMessage[]
                {
                    new GptMessage
                    {
                        Role = "system",
                        Text = promt,
                    },
                    /*new GptMessage
                    {
                        Role = "user",
                        Text = "Ура! Я готов к работе!",
                    },*/
                }
            };

            var requestJson = JsonSerializer.Serialize(requestModel);
            var requestContent = new StringContent(requestJson, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync("https://llm.api.cloud.yandex.net/foundationModels/v1/completion ", requestContent);

            if (response.StatusCode != System.Net.HttpStatusCode.OK)
            {
                _logger.LogError($"Gpt response status code: {response.StatusCode}");
                return string.Empty;
            }

            var jsonResponse = await response.Content.ReadAsStringAsync();

            var responseModel = JsonSerializer.Deserialize<GptResponse>(jsonResponse);

            if (responseModel == null)
            {
                _logger.LogError("Gpt response model is null");
                return string.Empty;
            }

            return responseModel.Result.Alternatives[0].Message.Text;
        }
    }
}
