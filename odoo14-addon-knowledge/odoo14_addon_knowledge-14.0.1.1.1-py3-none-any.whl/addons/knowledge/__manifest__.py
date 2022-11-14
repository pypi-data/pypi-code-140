# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Knowledge",
    "version": "14.0.1.1.1",
    "author": "OpenERP SA,"
    "MONK Software, "
    "Tecnativa, "
    "ForgeFlow, "
    "Odoo Community Association (OCA)",
    "category": "Knowledge",
    "development_status": "Production/Stable",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/knowledge",
    "depends": ["base"],
    "data": [
        "data/ir_module_category.xml",
        "security/knowledge_security.xml",
        "data/res_users.xml",
        "views/knowledge.xml",
        "views/res_config.xml",
    ],
    "demo": ["demo/knowledge.xml"],
    "installable": True,
    "application": True,
}
