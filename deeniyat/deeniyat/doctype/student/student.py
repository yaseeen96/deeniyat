# Copyright (c) 2024, yaseen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import dateutil


class Student(Document):
	
	def get_age(self):
		# calculate age from date of birth
		age_str = ""
		if self.dob:
			born = frappe.utils.getdate(self.dob)
			age = dateutil.relativedelta.relativedelta(frappe.utils.getdate(), born)
			age_str = str(age.years) + " year(s) " + str(age.months) + " month(s) " + str(age.days) + " day(s)"
		return age_str

	
	# override before_save method
	def before_save(self):
		# calculate age on save
		self.age = self.get_age()
	
	# custom function to receive total tests doctype data
	@frappe.whitelist()
	def get_total_tests():
		# Replace 'DocType1', 'DocType2', and 'DocType3' with the actual doctype names
		doctype1_count = frappe.db.count('Digar Azkar')
		doctype2_count = frappe.db.count('Fiqh us salaat Test')
		doctype3_count = frappe.db.count('Nazrah Quraan Test')

		total_count = doctype1_count + doctype2_count + doctype3_count

		return {
			"value": total_count,
			"fieldtype": "Currency",
			"route_options": {"from_date": "2023-05-23"},
			"route": ["query-report", "Permitted Documents For User"]
		}
