using BuyIn.Features.Player;

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
            Player player = new Player();
            player.BuildPlayer("hello", "world");    
        }
    }
}