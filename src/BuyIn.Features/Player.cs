namespace BuyIn.Features.Player
{
    using System.Reflection.Metadata.Ecma335;

    using BuyIn.Tools.RandomStr;

    public class Player
    {
        private string? playerFirstName;
        private string? playerLastName;
        private string playerId;

        /* Player name */
        public void SetPlayer(string firstName, string lastName)
        {
            if (String.IsNullOrWhiteSpace(firstName))
            {
                playerFirstName = "";
            }
            else 
            {
                playerFirstName = firstName;
            }
            if (String.IsNullOrWhiteSpace(lastName))
            {
                playerLastName = "";
            }
            else 
            {
                playerLastName = lastName;
            }
        }
        public string Showplayer()
        {
            if (String.IsNullOrEmpty(playerFirstName))
            {
                return "No player to show.";
            }
            else 
            {
                return playerFirstName + " " + playerLastName;
            }
        }

        /* Build the player (call all the methods) */
        public bool BuildPlayer(string firstName, string lastName)
        {
            SetPlayer(firstName, lastName);
            playerId = RandomString.GenerateUID();
            // add logic to make sure player id is set  
            return true;
        }
    }
}
