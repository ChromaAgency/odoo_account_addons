# Grupos de pagos.

Modulo realizado principalmente para la gestion de pagos de una factura a través de varios pagos.
Motivado por la necesidad de realizar recibos en Argentina.

El mismo debe de proveer la posibilidad de gestionar multiples pagos e imprimir un recibo de esos pagos.

## Test cases.

Para los proximos casos se espera que la factura y el pago queden completamente en 0, tanto en su monto en moneda local como el monto en moneda:

Los campos a revisar son "Amount residual" o monto adeudado de la factura.
amount_residual y amount_residual_currency de la linea del asiento contable.

Con la misma moneda que la factura y que la compañia.
* Pago del 100% de las factura en 1 solo pago.
* Pago del 100% de las factura en multiples pagos.
* Pago del 100% de las factura en multiples recibos.

Con distinta moneda que la factura o distinta moneda de la compañia (con diferentes rates) pero agregando marcar la factura como paga:
* Pago de las factura en 1 solo pago.
* Pago de las factura en multiples pagos.
* Pago de las factura en multiples recibos.

Deberia dar un saldo equivalente a la diferencia entre lo pagado en la moneda elegida y la factura:
* Pago parcial de la factura con la misma moneda.

No coincidira la diferencia entre pagado y factura pero deberia arrojar un saldo:
* Pago parcial de factura con diferente moneda.

Coincida el monto adeudado pero no el monto en ARS de la linea del asiento contable: 
* Pago parcial con la misma moneda, pero con diferentes tipos de cambio.

Pruebas a ejecutar, con empresa en ARS:
* Factura de 100 ARS. Pago de 100 ARS. -> Deberia quedar en 0.
* Factura de 100 ARS. 1 Pago de 10 ARS y 1 paog de 90 ars. -> Deberia quedar en 0.
* Factura de 100 ARS. 1 recibo de 40 ARS y 1 recibo de 60 ars. -> Deberia quedar en 0.
* Factura de 100 USD Con una tasa de 0,011. Con una tasa de 0,01 1 pago de 10.000 ARS pero Mark as fully paid.  -> Deberia quedar en 0.
* Factura de 100 USD Con una tasa de 0,011. Con una tasa de 0,01 1 pagos de 5.000 ARS y otro de 5100 pero Mark as fully paid.  -> Deberia quedar en 0.
* Factura de 100 USD Con una tasa de 0,011. Con una tasa de 0,01 1 recibos de 5.000 ARS y otro de 5100 pero el segundo Mark as fully paid. -> Deberia quedar en 0.
* Factura de 100 USD Con una tasa de 0,011. Con una tasa de 0,01 1 recibos de 5.000 ARS y otro de 3100 pero el segundo Mark as fully paid. -> Deberia quedar en 0.
* Factura de 10.000 ARS Con una tasa de 0,011. Con una tasa de 0,01 1 pago de 100 USD pero Mark as fully paid.  -> Deberia quedar en 0.
* Factura de 10.000 ARS Con una tasa de 0,011. Con una tasa de 0,01 2 pagos de 50 USD pero Mark as fully paid.  -> Deberia quedar en 0.
* Factura de 10.000 ARS Con una tasa de 0,011. Con una tasa de 0,01 2 recibos de 50 USD pero Mark as fully paid. -> Deberia quedar en 0
* Factura de 100 USD Con una tasa de 0,011. Con una tasa de 0,01 1 pago de 50 USD. -> Deberia quedar factura en 50, amount_residual_currency en 50, y amount_residual en un importe != 0.
* Factura de 100 USD Con una tasa de 0,011. Con una tasa de 0,01 1 pago de 5.000 USD. -> Deberia quedar factura en con adeudado != 0, amount_residual_currency != 0, y amount_residual en ~4090,90.
* Factura de 100 USD Con una tasa de 0,01. Con una tasa de 0,01 1 pago de 50 USD. -> Deberia quedar factura en 50, amount_residual_currency en 50, y amount_residual en un importe != 5000.
