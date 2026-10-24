namespace BuyIn.Features.Player
{
    using System.Reflection.Metadata.Ecma335;

    using BuyIn.Tools.RandomStr;

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
            }
            else 
            {
                this.playerFirstName = firstName;
            }
            if (String.IsNullOrWhiteSpace(lastName))
            {
                this.playerLastName = "";
            }
            else 
            {
                this.playerLastName = lastName;
            }
        }
    }
}
