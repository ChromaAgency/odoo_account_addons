from odoo.http import Controller, request, route, Response
from datetime import datetime 
class TxtController(Controller):

    @route('/l10n_ar_withholdings_afip_txt/comprobante_venta/<ids>', type='http', auth='user')
    def txt_comprobante_vta_route(self, ids):
        now = datetime.now()
        res = request.env['account.move'].browse([int(i) for i in ids.split(',')]).generate_ventas_comprobantes_txt()
        return Response(res, headers={
                "Content-Type": f"text/plain; charset=latin-1",

                'Content-Disposition':'attachment; filename="%s_%s_%s_comprobante_vta_%s.txt"' % (now.year, now.month, now.day, int(now.timestamp()) ) }, status=200)

    @route('/l10n_ar_withholdings_afip_txt/alicuotas_venta/<ids>', type='http', auth='user')
    def txt_alicuota_vta_route(self, ids):
        now = datetime.now()
        res = request.env['account.move'].browse([int(i) for i in ids.split(',')]).generate_ventas_alicuotas_txt()
        return Response(res, headers={
                "Content-Type": f"text/plain; charset=latin-1",

                'Content-Disposition':'attachment; filename="%s_%s_%s_alicuotas_vta_%s.txt"' % (now.year, now.month, now.day, int(now.timestamp()) ) }, status=200)
    
    @route('/l10n_ar_withholdings_afip_txt/alicuotas_compra/<ids>', type='http', auth='user')
    def txt_alicuota_compra_route(self, ids):
        now = datetime.now()
        res = request.env['account.move'].browse([int(i) for i in ids.split(',')]).generate_compras_alicuotas_txt()
        return Response(res, headers={
                "Content-Type": f"text/plain; charset=latin-1",

                'Content-Disposition':'attachment; filename="%s_%s_%s_alicuotas_compra_%s.txt"' % (now.year, now.month, now.day, int(now.timestamp()) ) }, status=200)
    
    @route('/l10n_ar_withholdings_afip_txt/comprobante_compra/<ids>', type='http', auth='user')
    def txt_alicuota_compra_route(self, ids):
        now = datetime.now()
        res = request.env['account.move'].browse([int(i) for i in ids.split(',')]).generate_compras_comprobantes_txt()
        return Response(res, headers={
                "Content-Type": f"text/plain; charset=latin-1",

                'Content-Disposition':'attachment; filename="%s_%s_%s_comprobante_vta_%s.txt"' % (now.year, now.month, now.day, int(now.timestamp()) ) }, status=200)