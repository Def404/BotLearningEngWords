# Обновление модели

```shell
dotnet ef dbcontext scaffold "Host=localhost;Database=learning_english_words;Username=adef;Password=199as55" Npgsql.EntityFrameworkCore.PostgreSQL --use-database-names --data-annotations --force  --context DatabaseContext  --output-dir Models --context-dir Data --schema profile
```
