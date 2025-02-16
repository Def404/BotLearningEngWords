using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System.Text;
using System.Text.Json;
using TelegramBot.Models;
using TelegramBot.Options;

namespace TelegramBot.Services
{
    public class YandexApiService
    {
        private readonly ILogger<YandexApiService> _logger;
        private readonly HttpClient _httpClient;
        private readonly YandexConfig _yandexConfig;

        public YandexApiService(ILogger<YandexApiService> logger, HttpClient httpClient, IOptions<YandexConfig> yandexConfig)
        {
            _logger = logger;
            _httpClient = httpClient;
            _yandexConfig = yandexConfig.Value;
        }

        public async Task<string> GenerateGtpMassageAsync(string prompt)
        {
            if (string.IsNullOrEmpty(_yandexConfig.FolderId) || string.IsNullOrEmpty(_yandexConfig.ApiToken))
            {
                _logger.LogError("No folder id or iam token provided");
                return string.Empty;
            }

            var requestModel = new GptRequest
            {
                ModelUri = $"gpt://{_yandexConfig.FolderId}/yandexgpt",
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
                        Text = prompt,
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

        public async Task<string> DetectLanguageAsync(string text)
        {
            if (string.IsNullOrEmpty(_yandexConfig.FolderId) || string.IsNullOrEmpty(_yandexConfig.ApiToken))
            {
                _logger.LogError("No folder id or iam token provided");
                return string.Empty;
            }

            var languageCodeHints = new string[] { "ru", "en" };

            var detectBodyModel = new DetectLangRequest
            {
                LanguageCodeHints = languageCodeHints,
                FolderId = _yandexConfig.FolderId,
                Text = text
            };

            var detectBodyJson = JsonSerializer.Serialize(detectBodyModel);

            var detectContent = new StringContent(detectBodyJson, Encoding.UTF8, "application/json");
            var detectResponse = await _httpClient.PostAsync("https://translate.api.cloud.yandex.net/translate/v2/detect", detectContent);

            if (detectResponse.StatusCode != System.Net.HttpStatusCode.OK)
            {
                _logger.LogError($"Detect response status code: {detectResponse.StatusCode}");
                return string.Empty;
            }

            var detectJsonResponse = await detectResponse.Content.ReadAsStringAsync();

            var detectResponseModel = JsonSerializer.Deserialize<DetectLangResponse>(detectJsonResponse);

            if (detectResponseModel == null)
            {
                _logger.LogError("Detect response model is null");
                return string.Empty;
            }

            return detectResponseModel.LanguageCode;
        }

        public async Task<string> TranslateAsync(string text, string targetLanguage)
        {
            if (string.IsNullOrEmpty(_yandexConfig.FolderId) || string.IsNullOrEmpty(_yandexConfig.ApiToken))
            {
                _logger.LogError("No folder id or iam token provided");
                return string.Empty;
            }

            var translateBodyModel = new TranslateRequest
            {
                FolderId = _yandexConfig.FolderId,
                TargetLanguageCode = targetLanguage,
                Texts = new string[] { text }
            };

            var translateBodyJson = JsonSerializer.Serialize(translateBodyModel);
            var translateContent = new StringContent(translateBodyJson, Encoding.UTF8, "application/json");

            var translateResponse = await _httpClient.PostAsync("https://translate.api.cloud.yandex.net/translate/v2/translate", translateContent);

            if (translateResponse.StatusCode != System.Net.HttpStatusCode.OK)
            {
                _logger.LogError($"Translate response status code: {translateResponse.StatusCode}");
                return string.Empty;
            }

            var translateJsonResponse = await translateResponse.Content.ReadAsStringAsync();
            var translateResponseModel = JsonSerializer.Deserialize<TranslateResponse>(translateJsonResponse);

            if (translateResponseModel == null)
            {
                _logger.LogError("Translate response model is null");
                return string.Empty;
            }

            return translateResponseModel.Translations[0].Text;
        }
    }
}
