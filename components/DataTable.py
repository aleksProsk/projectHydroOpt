import dash_table_experiments as dt
import dash_html_components as html
import numpy as np

from baseObjects import Restricted
CSafeNP = Restricted.CSafeNP
CSafeDF = Restricted.CSafeDF

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CDataTable(CDashComponent):
	def __init__(self, rows = [''], headers = [''], row_selectable = True, filterable = True, sortable = True, editable = False, style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.__np = CSafeNP(super().getUser())
		self.__df = CSafeDF(super().getUser())
		self.setTable(rows, headers, row_selectable, filterable, sortable, editable, style)
	def getRows(self): return self.__rows
	def getHeaders(self): return self.__headers
	def __setValues(self, rows):
		if rows == []:
			self.__values = []
		else:
			self.__values = self.__np.hstack(rows)
	def getValue(self):
		return self.__selected_rows
	def getData(self):
		return self.__df
	def update(self, selected_rows = None, rows = None):
		if selected_rows is not None:
			self.__selected_rows = selected_rows
		if rows is not None:
			self.__headers = list(rows[0].keys())
			self.__rows = []
			elems = []
			for row in rows:
				elems.append(list(row.values()))
			elems = self.__np.transpose(self.__np.array(elems))
			for elem in elems:
				self.__rows.append(self.__np.reshape(self.__np.array(elem), -1, 1))
			self.__setValues(self.__rows)
			self.__df.define(self.__values, columns=self.__headers)
	def setTable(self, rows, headers, row_selectable, filterable, sortable, editable, style):
		self.__setValues(rows)
		self.__df.define(self.__values, columns=headers)
		self.__selected_rows = []
		self.__dt = dt.DataTable(
			id=str(super().getID()),
			rows=self.__df.to_dict('records'),
			row_selectable=row_selectable,
			filterable=filterable,
			sortable=sortable,
			selected_row_indices=[],
			editable=editable,
		)
		self.__rows = rows
		self.__headers = headers
		super().setDashRendering(html.Div(self.__dt, style=style))
	def getRowsByIndices(self, indices):
		rows = []
		for i in indices:
			rows.append([])
			for column in self.__rows:
				rows[-1].append(column[i][0])
		return rows
	def addRow(self):
		for i in range(len(self.__rows)):
			self.__rows[i] = list(self.__rows[i])
			self.__rows[i].append([''])
		self.__setValues(self.__rows)
		self.__df.define(self.__values, columns=self.__headers)
		return self.__df.to_dict('records')