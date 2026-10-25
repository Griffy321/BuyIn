using BuyIn.Features.Player;
using BuyIn.Tools.Log;

namespace BuyIn
{
    public class RunProgram
    {
        public static void Main(string[] args)
        {
            // Player player = new Player();
            // Console.WriteLine("Enter a name");
            // string? name = Console.ReadLine();
            // player.SetPlayer(name);
            // player.Showplayer();
            Logger.Info(body: "App opened", resource: nameof(RunProgram));
            try
            {
                Player player = new Player("hello", "world");
            }
            catch (Exception ex)
            {
                // anything that wasn't handled elsewhere ends up here, so it gets logged before the app crashes
                Logger.Error(body: "Unhandled exception", resource: nameof(RunProgram), exception: ex);
                throw;
            }
            Logger.Info(body: "App closed", resource: nameof(RunProgram));
        }
    }
}