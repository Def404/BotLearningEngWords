using DatabaseClassLibrary.Models;
using Microsoft.EntityFrameworkCore;

namespace DatabaseClassLibrary.Data;

public partial class DatabaseContext : DbContext
{
    public DatabaseContext()
    {
    }

    public DatabaseContext(DbContextOptions<DatabaseContext> options)
        : base(options)
    {
    }

    public virtual DbSet<dictionary> dictionaries { get; set; }

    public virtual DbSet<user> users { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasPostgresExtension("uuid-ossp");

        modelBuilder.Entity<dictionary>(entity =>
        {
            entity.HasKey(e => e.uid).HasName("dictionary_pkey");

            entity.Property(e => e.uid).HasDefaultValueSql("uuid_generate_v4()");
            entity.Property(e => e.created).HasDefaultValueSql("now()");

            entity.HasOne(d => d.user_u).WithMany(p => p.dictionaries)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("dictionary_user_uid_fkey");
        });

        modelBuilder.Entity<user>(entity =>
        {
            entity.HasKey(e => e.uid).HasName("user_pkey");

            entity.Property(e => e.uid).HasDefaultValueSql("uuid_generate_v4()");
            entity.Property(e => e.created).HasDefaultValueSql("now()");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
