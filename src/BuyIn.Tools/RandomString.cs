namespace BuyIn.Tools.RandomStr
{
    public class RandomString
    {
        private const string AllowedChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";


        /// <summary>
        /// generates a random selection of numbers and charictes to be used as a uuid for any kind of relational opperation
        /// </summary>
        /// <param name="length"> default to 32</param>
        /// <returns></returns>
        public static string GenerateUID(int length = 32)
        {
            return Guid.NewGuid().ToString("N");
        }

        // / <summary>
        // / Generate a secure id that can be used for things like session ids 
        // / </summary>
        // / <param name="length"> default to 32</param>
        // / <returns></returns>
        public static string GenerateSecureUID(int length = 32)
        {
            return String.Create(length, AllowedChars, (buffer, chars) => 
            {
                System.Security.Cryptography.RandomNumberGenerator.GetItems(chars, buffer);
            });
        }
    }
}
