namespace TelegramBot.Models;

public class TranslateResponseModel
{
    public List<Translation> translations { get; set; }

    public class Translation
    {
        public string text { get; set; }
        public string detectedLanguageCode { get; set; }
    }
}