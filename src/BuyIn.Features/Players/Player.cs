namespace BuyIn.Features.Player
{
    using System.Reflection.Metadata.Ecma335;

    using BuyIn.Tools.RandomStr;
    using BuyIn.Tools.Log;

    public class Player
    {
        public string PlayerFirstName 
        {
            get {return field;} 
            init;
        }
        public string PlayerLastName 
        {
            get {return field;} 
            init;
        }
        public string PlayerId 
        {
            get {return field;} 
            init;
        } = RandomString.GenerateUID();

        public Player(string firstName, string lastName)
        {
            if (String.IsNullOrWhiteSpace(firstName))
            {
                this.PlayerFirstName = "";
                Logger.Warn(body: "Player created with a blank first name", resource: nameof(Player), attributes: new() { ["playerId"] = PlayerId });
            }
            else 
            {
                this.PlayerFirstName = firstName;
            }
            if (String.IsNullOrWhiteSpace(lastName))
            {
                this.PlayerLastName = "";
                Logger.Warn(body: "Player created with a blank last name", resource: nameof(Player), attributes: new() { ["playerId"] = PlayerId });
            }
            else
            {
                this.PlayerLastName = lastName;
            }
            Logger.Info(body: "Player created", resource: nameof(Player), attributes: new() { ["playerId"] = PlayerId });
        }
    }
}
