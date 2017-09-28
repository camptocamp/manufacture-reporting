# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from openerp import tools


class ReportMrpBomMatrix(models.Model):
    _name = 'report.mrp.bom.matrix'
    _auto = False

    component_id = fields.Many2one(comodel_name='product.product',
                                   string='Component Product', readonly=True)
    parent_template_id = fields.Many2one(comodel_name='product.template',
                                         string='Parent Product Template',
                                         readonly=True)
    parent_category_id = fields.Many2one(comodel_name='product.category',
                                         string='Parent Product Category',
                                         store=True, readonly=True)
    count_component_id = fields.Integer(string='# of Components/Parent '
                                               'Template', readonly=True)

    def _select(self):
        select_str = """
            SELECT min(l.id) as id, l.product_id as component_id,
                   p.product_tmpl_id as parent_template_id,                   
                   count(l.product_id) as count_component_id,
                   pt.categ_id as parent_category_id
        """
        return select_str

    def _from(self):
        from_str = """
            FROM mrp_bom_line as l
            INNER JOIN mrp_bom p
            ON p.id = l.bom_id
            INNER JOIN product_template pt
            on pt.id = p.product_tmpl_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY l.product_id,
                     p.product_tmpl_id
                     pt.categ_id
        """
        return group_by_str

    def _where(self):
        where_str = """"""
        return where_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
            )""" % (self._table, self._select(), self._from(), self._where(),
                    self._group_by()))
