using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DatabaseClassLibrary.Models;

[Table("dictionary", Schema = "profile")]
public partial class dictionary
{
    [Key]
    public Guid uid { get; set; }

    public Guid user_uid { get; set; }

    public string word { get; set; } = null!;

    public List<string>? translate { get; set; }

    public DateTime created { get; set; }

    public DateTime? modified { get; set; }

    [ForeignKey("user_uid")]
    [InverseProperty("dictionaries")]
    public virtual user user_u { get; set; } = null!;
}
