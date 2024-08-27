using Telegram.Bot.Types;
using Telegram.Bot;

namespace TelegramBot.Commands
{
    public class TestCmd : ICommand
    {
        public string Name => "Test";
        public string? Description => "/test [п1] [п2] - тестовая команда";

        public string Command => "/test";
        public int ParameterCount => 2;
       
        public async void Action(ITelegramBotClient botClient, Update update)
        {
            var massage = update.Message;

            if (massage == null)
                return;

            var user = massage.From;
            var chat = massage.Chat;

            if (massage.Text == null)
                return;

            var parameters = massage.Text
                .Replace(this.Command, "")
                .Trim()
                .Split(' ');


            if(parameters.Length < this.ParameterCount)
            {
                var errorMessage = $"У команды должны быть аргументы\n{this.Description}";
                await botClient.SendTextMessageAsync(chat.Id, $"{errorMessage}",
                replyToMessageId: massage.MessageId);

                return;
            }

            if (parameters.Length > this.ParameterCount) 
            {
                var errorMessage = $"У команды должны быть не больше 2 аргументов\n{this.Description}";
                await botClient.SendTextMessageAsync(chat.Id, $"{errorMessage}",
                replyToMessageId: massage.MessageId);

                return;
            }
          
            await botClient.SendTextMessageAsync(chat.Id, $"Команда выполнилась",
                replyToMessageId: massage.MessageId);
        }
    }
}
