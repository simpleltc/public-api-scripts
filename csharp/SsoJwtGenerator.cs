// These come from the System.IdentityModel.Tokens.Jwt nuget package
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Microsoft.IdentityModel.Tokens;

namespace SimpleLtc
{
    public class SsoJwtGenerator
    {
        // This should come from a secure location, but we will put it here for demonstration purposes.
        private const string mySecret = "TXlTU09TZWNyZXQ=";

        /// <summary>
        /// Generate a JWT given a username in the format username@companycode
        /// </summary>
        /// <param name="userId">User ID in the format username@companycode</param>
        /// <returns>The generated JWT</returns>
        public static string GenerateToken(string userId)
        {
            // For ease of copying the key from the SimpleLTC interface, the secret is Base64 encoded and must be decoded.
            byte[] decodedKey = Convert.FromBase64String(mySecret);

            var securityKey = new SymmetricSecurityKey(decodedKey);
            // Create signing credentials. This must use HMAC SHA-256
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            string epochTime = ((DateTimeOffset)DateTime.Now).ToUnixTimeSeconds().ToString();

            // Create a List of claims
            var claims = new List<Claim>();
            claims.Add(new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()));
            claims.Add(new Claim(JwtRegisteredClaimNames.Sub, userId));
            claims.Add(new Claim(JwtRegisteredClaimNames.Iat, epochTime));

            var jwt = new JwtSecurityToken(null, null,          // Issuer and audience are not supported and should be null
                            claims,
                            expires: DateTime.Now.AddDays(1),   // This is ignored by our token validation and will have a fixed expiration
                            signingCredentials: credentials);
            string jwt_token = new JwtSecurityTokenHandler().WriteToken(jwt);
            return jwt_token;
        }
    }
}
