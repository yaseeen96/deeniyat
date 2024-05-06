# Copyright (c) 2024, yaseen and contributors
# For license information, please see license.txt

from datetime import date
import frappe
from frappe.model.document import Document


class FiqhussalaatTest(Document):
	def validate(self):
		# Dynamically get all check fields in the DocType
		check_fields = [f.fieldname for f in frappe.get_meta(self.doctype).fields if f.fieldtype == 'Check']

		# Check if all check fields are checked
		all_checked = all(self.get(field) == 1 for field in check_fields)

		# Set the completion date to the current date if all check fields are checked and completion date is not already set
		if all_checked and not self.completion_date:
			self.completion_date = date.today()

