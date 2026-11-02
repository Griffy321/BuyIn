using BuyIn.Data.Config;
using BuyIn.Data.Write;
using BuyIn.Features.Player;
using BuyIn.Features.PlayerRepository;




var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

Setup.CreateTable(PlayerData.DbName, PlayerData.TableName, typeof(Player), nameof(Player.PlayerId));

app.MapPost("/players", (CreatePlayerRequest req) =>
{
    var player = new Player(req.FirstName, req.LastName);
    bool isPlayerInserted = Insert.WriteRecord(PlayerData.DbName, PlayerData.TableName, player);
    if (isPlayerInserted)
    {
        return Results.Ok(new CreatePlayerResponse(player.PlayerId));
    }
    else
    {
        return Results.Problem(
            detail: "Failed to create the user.",
            statusCode: StatusCodes.Status500InternalServerError,
            title: "Server error"
        );
    }
});

app.Run();

public record CreatePlayerRequest(string FirstName, string LastName);
public record CreatePlayerResponse(string PlayerId);
public record PlayerResponse(string PlayerId, string FirstName, string LastName);
