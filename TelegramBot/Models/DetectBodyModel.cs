namespace TelegramBot.Models;

public class DetectBodyModel
{
    public string folderId {get; set;}
    public string[] languageCodeHints {get; set;}
    public string text {get; set;}

    public DetectBodyModel(string folderId, string[] languageCodeHints, string text)
    {
        this.folderId = folderId;
        this.languageCodeHints = languageCodeHints;
        this.text = text;
    }
}