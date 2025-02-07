using Telegram.Bot.Polling;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;

namespace TelegramBot.Handlers
{
    public interface ITelegramHandlers
    {
        Task OnError(Exception exception, HandleErrorSource source);
        Task OnMessage(Message msg, UpdateType type);
        Task OnUpdate(Update update);
    }
}
