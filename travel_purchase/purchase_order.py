# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.addons.travel.res_config import get_alert_address


class purchase_order(orm.Model):
    _inherit = 'purchase.order'

    def _get_responsible_emails(
            self, cr, uid, ids, name=None, args=None, context=None):
        context = context or {}
        res = {}

        for po in self.browse(cr, uid, ids, context=context):
            if po.state == 'approved' and po.travel_id is not False:
                ctx = dict(context, alert_type='opened')
                res[po.id] = get_alert_address(
                    self.pool.get("ir.config_parameter"), cr, uid, context=ctx)

        return res

    _columns = {
        'travel_id': fields.many2one('travel.travel', string="Travel"),
        'responsible_emails': fields.function(_get_responsible_emails,
                                              type='char',
                                              string='Responsible e-mails'),
    }
