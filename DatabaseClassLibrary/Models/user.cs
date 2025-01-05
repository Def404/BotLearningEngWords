using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DatabaseClassLibrary.Models;

[Table("user", Schema = "profile")]
[Index("telegram_user_id", Name = "unq_telegram_user_id", IsUnique = true)]
public partial class user
{
    [Key]
    public Guid uid { get; set; }

    public long telegram_user_id { get; set; }

    public string telegram_user_name { get; set; } = null!;

    public DateTime created { get; set; }

    public DateTime? modified { get; set; }

    [InverseProperty("user_u")]
    public virtual ICollection<dictionary> dictionaries { get; set; } = new List<dictionary>();
}
