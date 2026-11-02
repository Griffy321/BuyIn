using BuyIn.Data.Config;
using BuyIn.Data.Write;
using BuyIn.Features.Player;
using BuyIn.Features.PlayerRepository;


var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

Setup.CreateTable(PlayerData.DbName, PlayerData.TableName, typeof(Player), nameof(Player.PlayerId));

app.MapPost("/players", (CreatePlayerRequest req) => // post has a body
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

app.MapGet("/players/{playerId}", (string playerId) => // get has no body so jus ttakes a player id in the lambda
{
    try
    {
        var data = PlayerData.GetPlayerInfo(playerId);
        if (data is not null)
        {
            return Results.Ok(new PlayerResponse(data.PlayerId, data.PlayerFirstName, data.PlayerLastName));
        }
        else
        {
            // no player with that id: the app forgets its saved id when it gets a 404
            return Results.Problem(
                detail: $"No player with id {playerId}.",
                statusCode: StatusCodes.Status404NotFound,
                title: "Player not found"
            );
        }
    }
    catch // the repository already logged the exception, so it isn't needed here
    {
        // something broke on our side: the app keeps its saved id and shows an error when it gets a 500
        return Results.Problem(
            detail: "Failed to read the player.",
            statusCode: StatusCodes.Status500InternalServerError,
            title: "Server error"
        );
    }
});

app.Run();

public record CreatePlayerRequest(string FirstName, string LastName);
public record CreatePlayerResponse(string PlayerId);
public record PlayerResponse(string PlayerId, string FirstName, string LastName);
