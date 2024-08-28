namespace TelegramBot.Commands
{
    internal class CommandService
    {
        public static string[] GetParameters(string messageText, string command)
        {
            var parameters = messageText
               .Replace(command, "")
               .Trim()
               .Split(' ');

            return parameters;
        }
    }
}
