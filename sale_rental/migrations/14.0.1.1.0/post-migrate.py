# Copyright 2009-2023 Noviat (https://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    rental_products = env["product.template"].search(
        [("rented_product_tmpl_id", "!=", False)]
    )
    rental_uom_category = env.ref("sale_rental.uom_categ_rental_time")
    day_uom = env.ref("uom.product_uom_day")
    hour_uom = env.ref("uom.product_uom_hour")
    new_hour_uom = env.ref("sale_rental.sale_rental_product_uom_hour")
    new_day_uom = env.ref("sale_rental.sale_rental_product_uom_day")
    new_week_uom = env.ref("sale_rental.sale_rental_product_uom_week")
    new_month_uom = env.ref("sale_rental.sale_rental_product_uom_month")
    new_year_uom = env.ref("sale_rental.sale_rental_product_uom_year")
    rental_products.filtered(
        lambda rp: rp.uom_id == day_uom and rp.uom_po_id == day_uom
    ).write({"uom_id": new_day_uom.id, "uom_po_id": new_day_uom.id})
    for rental_product in rental_products.filtered(
        lambda rp: rp.uom_id == day_uom and rp.uom_po_id != day_uom
    ):
        if rental_product.uom_po_id.category_id != rental_uom_category:
            po_uom_name = rental_product.uom_po_id.name
            if rental_product.uom_po_id == hour_uom:
                rental_product.write({"uom_po_id": new_hour_uom.id})
            elif "Week" in po_uom_name or "week" in po_uom_name:
                rental_product.write({"uom_po_id": new_week_uom.id})
            elif "Month" in po_uom_name or "month" in po_uom_name:
                rental_product.write({"uom_po_id": new_month_uom.id})
            elif "Year" in po_uom_name or "year" in po_uom_name:
                rental_product.write({"uom_po_id": new_year_uom.id})
            else:
                _logger.error(
                    "No corresponding UOM was found for the product %s"
                    % (rental_product.name,)
                )
