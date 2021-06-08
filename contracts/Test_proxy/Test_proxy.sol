// SPDX-License-Identifier: MIT

// Test proxy
// Este es un contrato que sirve para hacer "proxy" con otros contratos.
// ¿Porqué?
// Para probar la funcionalidad cuando tx.orign != msg.sender
// Es decir, para ver que ocurre cuando llamamos a un contrato desde otro.

pragma solidity >=0.6.6;
 
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

contract TestProxy {

   // El text llama a una direccion de un token ERC20
   // para probar qué ocurre. Se construye con la direccion del contrato.

   constructor(address tokenaddr) {
       token = tokenaddr;
   }
   
   address public immutable token;

   event ProxyLog(address, string);
   event ProxyLogBoolResult(string, bool);

   // Llama a la funcion authorize del contrato subyacente
   function proxy_approve(address spender, uint256 amount) public returns (bool) {
      emit ProxyLog(token, "Emitiendo ERC20 approve");
      emit ProxyLogBoolResult("Resultado ERC20 approve",  ERC20(token).approve(spender, amount));
   }

   function proxy_transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
      emit ProxyLog(token, "Emitiendo ERC20 transferFrom");
      emit ProxyLogBoolResult("Resultado ERC20 transferFrom",  ERC20(token).approve(sender, amount));
   }

}
