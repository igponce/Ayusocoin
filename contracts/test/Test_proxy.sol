// SPDX-License-Identifier: MIT

// Test proxy
// Este es un contrato que sirve para hacer "proxy" con otros contratos.
// ¿Porqué?
// Para probar la funcionalidad cuando tx.orign != msg.sender
// Es decir, para ver que ocurre cuando llamamos a un contrato desde otro.
   
pragma solidity >=0.7.0;

import "../../interfaces/IERC20.sol";

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
      emit ProxyLogBoolResult("Resultado ERC20 approve", iERC20(token).approve(spender, amount));
   }

   function proxy_transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
      emit ProxyLog(token, "Emitiendo ERC20 transferFrom");
      emit ProxyLogBoolResult("Resultado ERC20 transferFrom", iERC20(token).approve(sender, amount));
   }

}
