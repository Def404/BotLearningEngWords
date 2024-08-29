namespace TelegramBot.Commands
{
    internal static class CommandService
    {
        public static string[] GetParameters(string messageText, string command)
        {
            var parameters = messageText
                .Replace(command, "")
                .Trim()
                .Split(' ');

            parameters = parameters.Where(x => !string.IsNullOrWhiteSpace(x)).ToArray();

            return parameters;
        }

        public static string GetParameterForTranslate(string messageText, string command)
        {
            var parameter = messageText
                .Replace(command, "")
                .Trim();

            return parameter;
        }
    }
}