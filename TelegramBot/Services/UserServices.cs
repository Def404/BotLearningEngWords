using DatabaseClassLibrary.Data;
using DatabaseClassLibrary.Models;
using Microsoft.EntityFrameworkCore;
using Telegram.Bot.Types;

namespace TelegramBot.Services
{
    public class UserServices
    {
        private readonly DatabaseContext _context;

        public UserServices(DatabaseContext context)
        {
            _context = context;
        }

        public async Task<bool> InitUser(User tgUser)
        {
            var userInDb = await _context.users.FirstOrDefaultAsync(i => i.telegram_user_id == tgUser.Id);
            if (userInDb == null)
            {
                var newUser = new user
                {
                    telegram_user_id = tgUser.Id,
                    telegram_user_name = tgUser.Username ?? tgUser.FirstName,
                    created = DateTime.UtcNow,
                };

                await _context.users.AddAsync(newUser);
                var result = await _context.SaveChangesAsync();

                return result > 0;
            }

            return false;
        }

        public async Task<bool> HasUserAsync(User tgUser)
        {
            var userInDb = await _context.users.FirstOrDefaultAsync(i => i.telegram_user_id == tgUser.Id);

            return userInDb != null;
        }

        public async Task<List<user>> GetAllUsersAsync()
        {
            return await _context.users.ToListAsync();
        }

        public async Task<bool> DeleteUserAsync(User tgUser)
        {
            var userInDb = await _context.users.FirstOrDefaultAsync(i => i.telegram_user_id == tgUser.Id);
            if (userInDb != null)
            {
                _context.users.Remove(userInDb);
                var result = await _context.SaveChangesAsync();
                return result > 0;
            }
            return false;
        }
    }
}
