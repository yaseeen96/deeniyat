# Copyright (c) 2024, yaseen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Teachers(Document):

	def create_user(self):

		# create a new user wizth role_profile 'Teacher'
		# and assign it to the teacher
		if frappe.db.exists("User", self.email):
			frappe.msgprint("A user with this email address already exists.")
		else:
			user = frappe.get_doc({
				"doctype": "User",
				"email": self.email,
				"first_name": self.name1,
				"roles": [
					{
						"doctype": "Has Role", 
						"role": "Teacher"
					}
				]
			}).insert()
			
			frappe.msgprint("A user was created with email "+ self.email)

	def before_save(self):
		# create a user on save
		self.create_user()

	def after_delete(self):
		# delete the user on delete
		frappe.delete_doc("User", self.email)