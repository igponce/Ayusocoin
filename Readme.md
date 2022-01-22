# Ayusocoin

¿Qué es?

Este es un ejemplo de "moneda" (un token de Ethereum) que se distribuye
a varios cargos públicos españoles para que tengan una toma de contacto
de primera mano con las criptomonedas y los contratos inteligentes (smart contracts).

El token implementa el estandar ERC20 de Ethereum.

Está escrito a mano desde cero, sin utilizar librerías (como OpenZeppelin) para que alguien que no ha visto nunca el código de un Token de Ethereum pueda entenderlo.

Datos curiosos:

- Hay un total de 47.000 millones de Ayusos en circulación.
- Tocamos a 1000 ayusos por cada español ;-)
- Un Ayuso puede tener hasta 6 decimales, en vez de los 2 decimales del Euro.
- ¿Porqué seis decimales? porque sí.

La circulación total es de 47 mil millones de tokens (tocamos a 1000 ayusos por cada español).
Y admite 6 decimales.

## Fases

### 1 - Fase inicial - distribución limitada

En la primera fase se mandan varias 'paper wallet' de Ethereum a distintos políticos españoles **sin contraprestación alguna**.
El hecho de recibir estas paper wallet no supone la aceptación de estos Tokens.
Para aceptar un token de forma efectiva, la dirección tiene que disponer de Ethereum y transferir esos tokens a otra dirección... 

El valor del token al enviarse es de cero (0) euros.

### 2 - Faucet

En una segunda fase el token se pone a disposición de todos los usuarios de la red Ethereum.
El mecanismo de distribución es un "Faucet", que consiste en que cada interesado puede solicitar de un *smart contract* que se le envíen por una sola vez una cantidad de Ayusos (limitado a 1000 por dirección).
El coste de recibir de esos Ayusos es a cargo del interesado, y consiste exclusivamente en el pago a los mineros del "gas" (medido en "gwei") que se utiliza en el *smart contract*.


Para saber el valor del "gas" en el momento de interactuar con el contrato desde el "Faucet", se puede consultar su valor aproximado en: 
 - https://etherscan.io/gastracker

Durante esta fase para evitar el acopio de Tokens, se ha limitado el número de tokens por cada dirección ethereum a 10.000. 


### 3 - AirDrop / Reduccion de volumen

De los AYusoCoins restantes que no se hayan solicitado y que quedan por repartir, el 50% se repartirá entre los "holders" (wallets que tengan en ese momento AYusoCoins en su poder), obteniendo así un "Plus" por la confianza demostrada en la moneda y el otro 50% restante se entregará a un exchange, para que sea más facil su salida a mercado y poder obtener y/o vender las AYusoCoins más facilmente.


### 4 - Salida a Mercado

La forma mas sencilla y facil de adquirir tokens/monedas es la de utilizar un "exchange" o mercado, en la que se pueden adquirir monedas con dinero real (euros o dolares) y según la demanda/oferta que tenga la moneda, esta aumentará su valor o bajará, los mercados mas famosos y faciles de usar, ya que solo requieren de una aplicación móvil son:

 - Crypto.com
 - Binance
 - Coinbase

Los AYusoCoin saldrán a mercado a una fecha próxima o igual al 12 de Octubre, coincidiendo con el "Día de la Hispanidad", ya que es una fiesta nacional reconocida de nuestro pais y la ideal para el lanzamiento de esta moneda. ( https://es.wikipedia.org/wiki/Fiesta_Nacional_de_Espa%C3%B1a )



## Como desplegar y testear

### Paso 1: Blockchain

Para test / desarrollo de DAPP hay que tener un blockchain de prueba en funcionamiento.

Para esto hay que ejecutar:

```
brownie console
```

Eth-brownie despliega un blockchain de test con las direcciones de los contratos y una de test listas para usarse.


### Paso 2: Despliegue de contratos

Los contratos se despliegan ejecutando:

```
brownie run deploy --network development|mainnet|ropsten
```

Si queremos desplegar un contrato usando una dirección concreta tenemos que crear la variable de entorno PRIVATE_KEY con la clave privada (en hexadecimal) correspondiente a la wallet desde la que desplegamos los contratos.

