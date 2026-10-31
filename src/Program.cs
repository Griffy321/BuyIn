using BuyIn.Features.Player;
using BuyIn.Tools.Log;
using BuyIn.Data.Config;
using BuyIn.Data.Write;


namespace BuyIn
{
    public class RunProgram
    {
        public static void Main(string[] args)
        {
            Logger.Info(body: "App opened", resource: nameof(RunProgram));
            try
            {
                Player player = new Player("hello", "world");
                Insert.GetMetaData(player);
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