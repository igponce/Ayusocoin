var SimpleVoting;

window.onload = function() {

     $.getJSON("./contracts/Airdrop.json", 
         function(json) {
            Airdrop = TruffleContract( json );
            Airdrop.setProvider(
               new Web3.providers.HttpProvider(
                 "http://localhost:8545"));

}

function DisplayBalance() {
   Ayusocoin.deployed()
      .then(token => token.balanceOf());
}

function ClaimAirdrop() {

   Airdrop.deployed()
      .then(instance => instance.Claim())
      .catch();


}


