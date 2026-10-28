namespace BuyIn.Features.Player
{
    using System.Reflection.Metadata.Ecma335;

    using BuyIn.Tools.RandomStr;
    using BuyIn.Tools.Log;

    public class Player
    {
        public string playerFirstName 
        {
            get {return field;} 
            init;
        }
        public string playerLastName 
        {
            get {return field;} 
            init;
        }
        public string playerId 
        {
            get {return field;} 
            init;
        } = RandomString.GenerateUID();

        public Player(string firstName, string lastName)
        {
            if (String.IsNullOrWhiteSpace(firstName))
            {
                this.playerFirstName = "";
                Logger.Warn(body: "Player created with a blank first name", resource: nameof(Player), attributes: new() { ["playerId"] = playerId });
            }
            else 
            {
                this.playerFirstName = firstName;
            }
            if (String.IsNullOrWhiteSpace(lastName))
            {
                this.playerLastName = "";
                Logger.Warn(body: "Player created with a blank last name", resource: nameof(Player), attributes: new() { ["playerId"] = playerId });
            }
            else
            {
                this.playerLastName = lastName;
            }
            Logger.Info(body: "Player created", resource: nameof(Player), attributes: new() { ["playerId"] = playerId });
        }
    }
}
