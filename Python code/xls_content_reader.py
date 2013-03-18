import xlrd
import numpy

workbook = xlrd.open_workbook('OWCSheet45843.xls')
#assume there is one sheet and it is named as Sheet1
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1

"""
the important columns within the xls file are
Tarih
Valor (that is the turkish oe in it)
Aciklama (again the turkish ch is there)
Tutar
Kontrat numarasi (the turkish i without the dot)

"""


while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    print 'Row:', curr_row
    curr_cell = -1
    while curr_cell < num_cells:
        curr_cell += 1
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        cell_type = worksheet.cell_type(curr_row, curr_cell)
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        print '	', cell_type, ':', cell_value
    
