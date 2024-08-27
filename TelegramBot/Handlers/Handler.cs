using Microsoft.Extensions.Logging;
using NLog.Extensions.Logging;

namespace TelegramBot.Handlers;

public class Handler
{
    protected static readonly ILogger MyLogger = LoggerFactory
        .Create(builder => builder.AddNLog())
        .CreateLogger<Handler>();
}