namespace BuyIn.Features.SessionPlayer
{
    using BuyIn.Tools.RandomStr;
    
    class SessionPlayer
    {
        private List<decimal> _buyins;
        private Decimal _cashOut;
        private string _status;
        private bool _isSettled;
        private DateTime _joinedAt = new DateTime();
        private DateTime _leftAt = new DateTime();

        // public DateTime SetJoinedAt(string playerId)
        // {
        //     return playerId
        // }
    }
}