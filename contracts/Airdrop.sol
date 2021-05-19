// Airdrop contract

// Para no tener que dar uno a uno los tokens, tenemos este contrato de Airdrop.
//
// ¿Qué es un Airdrop? es una forma muy común de distribuir nuevos Tokens.
//
// Consiste en un contrato (que _suele_ tener una página web asociada)
// que distribuye los tokens a quien los solicita.
// Así el que crea el token no tiene que pagar por distribuir los tokens,
// y sólo los interesados 'pagan' a los mineros de la red por el coste de la transacción.

pragma solidity =0.6.6;
 
interface ERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract Airdrop {

   // Vamos a hacer un Airdrop _muy_ sencillo:
   //   - No podemos saber de qué país es cada dirección así que:
   //   - Cada dirección de Ethereum debe poder participar en el Airdrop.
   //   - A cada dirección que lo solicite le transferimos 1000 unidades del tocken.
   //   - Sólo se puede participar en el airdrop una sola vez. 
   //   - Si hay algún problema, la transacción _falla_
   
   // Primero necesitamos la dirección del contrato del Token
   
   address public immutable token;

   // También necesitamos una lista de direcciones.
   // Un "mapping" direccion -> a un 0 o 1 bastaría...
   // .. pero ese tipo de dato no existe en este lenguaje)
   // .. así que hay que construirlo a mano.

   // este es un bitmap (hay formas más eficientes de hacerlo, pero esta nos sirve)   
   mapping (address => uint256) public claimed;
   uint256 public immutable claimAmount;

   event Claimed(address _by, address _to, uint256 _value);
   
   // Una dirección pública son 160 bits la "parte de arriba" estará a 0.
   function isClaimed(address index) public view returns (uint256) {
       return claimed[index];
   }
      
   function _setClaimed(address index) private {
       claimed[index] = claimAmount;
   }
   
   // Esta funcion es la que permite reclamar los tokens.
   // No hace falta ser el dueño de la dirección para solicitarlo.
   // De todos modos... ¿quién puede querer enviar tokens a otro?
   // Hmm.. ¿puede haber alguna implicación legal de eso?
   
   function Claim(address index) public returns (uint256) {
      // hmm... ¿dejamos que lo haga un contrato?  require(msg.sender == tx.origin, "Only humans");
      require(isClaimed(index) == 0);
      _setClaimed(index);
      // Hacemos la transferencia y revertimos operacion si da algún error
      require(ERC20(token).transfer(index, claimAmount), "Airdrop: error transferencia");
      emit Claimed(msg.sender, index, claimAmount);
      return claimAmount;
   }
   
   // Necesitamos construir el contrato (instanciar)
   // Constructor

   constructor(address tokenaddr, uint256 claim_by_addr) public {
       token = tokenaddr;
       claimAmount = claim_by_addr;
   }

}
