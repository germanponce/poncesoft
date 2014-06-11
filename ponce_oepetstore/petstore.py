
from openerp.osv import osv, fields

class message_of_the_day(osv.osv):
    _name = "message_of_the_day"

    def my_method(self, cr, uid, context=None):
        return {"hello": "world"}
    
    _columns = {
        'message': fields.text(string="Message"),
        'color': fields.char(string="Color", size=20),
    }


class product(osv.osv):
    _inherit = "product.product"
    
    _columns = {
        'max_quantity': fields.float(string="Max Quantity"),
    }

