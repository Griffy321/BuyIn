namespace BuyIn.Features.SessionPlayer
{
    using BuyIn.Tools.RandomStr;
    
    class SessionPlayer
    {
        private List<decimal> buyins;
        private Decimal cashOut;
        private string status;
        private bool isSettled;
        private DateTime joinedAt = new DateTime();
        private DateTime leftAt = new DateTime();

        // public DateTime SetJoinedAt(string playerId)
        // {
        //     return playerId
        // }
    }
}