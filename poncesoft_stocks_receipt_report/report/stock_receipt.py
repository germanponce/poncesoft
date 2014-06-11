# -*- coding: utf-8 -*-

from report import report_sxw

class stock_receipt_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name,context=None): 
        super(stock_receipt_report, self).__init__(cr, uid, name, context=context) 
        self.localcontext.update({ 
        })
    

report_sxw.report_sxw( 
    'report.stock.picking.out',
    'stock.picking.out',
    'poncesoft_stocks_receipt_report/report/stock_receipt.rml',
    parser=stock_receipt_report,
    header=False
)
