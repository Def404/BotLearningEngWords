namespace TelegramBot.Models;

public class TranslateBodyModel
{
    public string targetLanguageCode {get; set;}
    public string[] texts {get; set;}
    public string folderId {get; set;}
    
    public TranslateBodyModel(string folderId, string targetLanguageCode, string text)
    {
        this.folderId = folderId;
        this.targetLanguageCode = targetLanguageCode;
        this.texts = new string[] { text };
    }

}