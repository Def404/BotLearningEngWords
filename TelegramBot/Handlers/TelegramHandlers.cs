using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Telegram.Bot;
using Telegram.Bot.Polling;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;
using TelegramBot.Commands.Interfaces;
using TelegramBot.Services;

namespace TelegramBot.Handlers
{
    public class TelegramHandlers : ITelegramHandlers
    {
        private readonly CancellationTokenSource _cts;
        private readonly TelegramBotClient _bot;
        private readonly User _me;
        private readonly IServiceProvider _services;
        private readonly ILogger _logger;

        public TelegramHandlers(CancellationTokenSource cts, TelegramBotClient bot, User me, IServiceProvider services)
        {
            _cts = cts;
            _bot = bot;
            _me = me;
            _services = services;
            _logger = services.GetRequiredService<ILogger<TelegramHandlers>>();
        }

        public async Task OnError(Exception exception, HandleErrorSource source)
        {
            _logger.LogError(exception, $"Error from {source}");

            await Task.Delay(2000, _cts.Token);
        }

        public async Task OnMessage(Message msg, UpdateType type)
        {
            if (msg.Text is not { } text)
                _logger.LogWarning($"Received a message of type {msg.Type}");
            else if (text.StartsWith('/'))
            {
                var space = text.IndexOf(' ');
                if (space < 0) space = text.Length;
                var command = text[..space].ToLower();
                if (command.LastIndexOf('@') is > 0 and int at) // it's a targeted command
                    if (command[(at + 1)..].Equals(_me.Username, StringComparison.OrdinalIgnoreCase))
                        command = command[..at];
                    else
                        return; // command was not targeted at me
                await OnCommand(command, text[space..].TrimStart(), msg);
            }
            else
                await OnTextMessage(msg);
        }

        async Task OnTextMessage(Message msg)
        {
            _logger.LogInformation($"Received text '{msg.Text}' in {msg.Chat}");
            await OnCommand("/start", "", msg); // for now we redirect to command /start
        }

        async Task OnCommand(string command, string args, Message msg)
        {
            _logger.LogInformation($"Received command: {command} {args}");

            try
            {
                var userService = _services.GetRequiredService<UserServices>();
                var tgUser = msg.From;

                if (tgUser == null)
                {
                    await _bot.SendMessage(msg.Chat, "Ошибка пользователя");
                }
                else
                {
                    var initUser = await userService.InitUser(tgUser);

                    if (initUser)
                    {
                        await _bot.SendMessage(msg.Chat, $"Вы успешно зарегистрировались в системе!");
                    }

                    var commands = _services.GetServices<ICommand>();
                    var myCommand = commands.FirstOrDefault(i => i.CommandTag.Equals(command));
                    if (myCommand is not null)
                    {
                        await myCommand.Action(_bot, msg);
                    }
                    else
                    {
                        await _bot.SendMessage(msg.Chat, "Команда не найдена");
                    }
                }
            }
            catch (Exception ex)
            {

                _logger.LogError(ex.Message);
            }
        }

        public async Task OnUpdate(Update update)
        {
            switch (update)
            {
                case { CallbackQuery: { } callbackQuery }: await OnCallbackQuery(callbackQuery); break;
                case { PollAnswer: { } pollAnswer }: await OnPollAnswer(pollAnswer); break;
                default: _logger.LogInformation($"Received unhandled update {update.Type}"); break;
            };
        }

        async Task OnCallbackQuery(CallbackQuery callbackQuery)
        {
            await _bot.AnswerCallbackQuery(callbackQuery.Id, $"You selected {callbackQuery.Data}");
            await _bot.SendMessage(callbackQuery.Message!.Chat, $"Received callback from inline button {callbackQuery.Data}");
        }

        async Task OnPollAnswer(PollAnswer pollAnswer)
        {
            if (pollAnswer.User != null)
                await _bot.SendMessage(pollAnswer.User.Id, $"You voted for option(s) id [{string.Join(',', pollAnswer.OptionIds)}]");
        }
    }
}
