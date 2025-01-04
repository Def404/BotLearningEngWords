using Telegram.Bot;
using Telegram.Bot.Polling;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;

namespace TelegramBot.Handlers
{
    public class TelegramHandlers : ITelegramHandlers
    {
        private readonly CancellationTokenSource _cts;
        private readonly TelegramBotClient _bot;
        private readonly User _me;

        public TelegramHandlers(CancellationTokenSource cts, TelegramBotClient bot, User me)
        {
            _cts = cts;
            _bot = bot;
            _me = me;
        }

        public async Task OnError(Exception exception, HandleErrorSource source)
        {
            Console.WriteLine(exception);
            await Task.Delay(2000, _cts.Token);
        }

        public async Task OnMessage(Message msg, UpdateType type)
        {
            if (msg.Text is not { } text)
                Console.WriteLine($"Received a message of type {msg.Type}");
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
            Console.WriteLine($"Received text '{msg.Text}' in {msg.Chat}");
            await OnCommand("/start", "", msg); // for now we redirect to command /start
        }

        async Task OnCommand(string command, string args, Message msg)
        {
            Console.WriteLine($"Received command: {command} {args}");

            foreach (var myCommand in CommandsList.Commands.Where(c => command.Equals(c.CommandTag)))
            {
                await myCommand.Action(_bot, msg);
            }

            /*switch (command)
            {
                case "/start":
                    await _bot.SendMessage(msg.Chat, """
                <b><u>Bot menu</u></b>:
                /photo [url]    - send a photo <i>(optionally from an <a href="https://picsum.photos/310/200.jpg">url</a>)</i>
                /inline_buttons - send inline buttons
                /keyboard       - send keyboard buttons
                /remove         - remove keyboard buttons
                /poll           - send a poll
                /reaction       - send a reaction
                """, parseMode: ParseMode.Html, linkPreviewOptions: true,
                        replyMarkup: new ReplyKeyboardRemove()); // also remove keyboard to clean-up things
                    break;
                case "/help":
                    var c = CommandsList.Commands.Find(i => i.CommandTag == "/help");
                    await c.Action(_bot, msg);
                   
                    break;
                case "/photo":
                    if (args.StartsWith("http"))
                        await _bot.SendPhoto(msg.Chat, args, caption: "Source: " + args);
                    else
                    {
                        await _bot.SendChatAction(msg.Chat, ChatAction.UploadPhoto);
                        await Task.Delay(2000); // simulate a long task
                        await using var fileStream = new FileStream("bot.gif", FileMode.Open, FileAccess.Read);
                        await _bot.SendPhoto(msg.Chat, fileStream, caption: "Read https://telegrambots.github.io/book/");
                    }
                    break;
                case "/inline_buttons":
                    var inlineMarkup = new InlineKeyboardMarkup()
                        .AddNewRow("1.1", "1.2", "1.3")
                        .AddNewRow()
                            .AddButton("WithCallbackData", "CallbackData")
                            .AddButton(InlineKeyboardButton.WithUrl("WithUrl", "https://github.com/TelegramBots/Telegram.Bot"));
                    await _bot.SendMessage(msg.Chat, "Inline buttons:", replyMarkup: inlineMarkup);
                    break;
                case "/keyboard":
                    var replyMarkup = new ReplyKeyboardMarkup()
                        .AddNewRow("1.1", "1.2", "1.3")
                        .AddNewRow().AddButton("2.1").AddButton("2.2");
                    await _bot.SendMessage(msg.Chat, "Keyboard buttons:", replyMarkup: replyMarkup);
                    break;
                case "/remove":
                    await _bot.SendMessage(msg.Chat, "Removing keyboard", replyMarkup: new ReplyKeyboardRemove());
                    break;
                case "/poll":
                    await _bot.SendPoll(msg.Chat, "Question", ["Option 0", "Option 1", "Option 2"], isAnonymous: false, allowsMultipleAnswers: true);
                    break;
                case "/reaction":
                    await _bot.SetMessageReaction(msg.Chat, msg.Id, ["❤"], false);
                    break;
            }*/
        }

        public async Task OnUpdate(Update update)
        {
            switch (update)
            {
                case { CallbackQuery: { } callbackQuery }: await OnCallbackQuery(callbackQuery); break;
                case { PollAnswer: { } pollAnswer }: await OnPollAnswer(pollAnswer); break;
                default: Console.WriteLine($"Received unhandled update {update.Type}"); break;
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
