# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 15:31:15 2021

@author: Egon
"""
import sys
import os
from sql import *
import re
from datetime import time, date
from PyQt5.QtCore import QTranslator, QDate, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QApplication, QTableWidgetItem, QMessageBox
from PyQt5 import uic
from pdfgen import canvas 
from reportFile import reportObj
import purchase
from decimal import *
from ErrorLogger import *
import traceback

getcontext().prec = 20

try:
    os.mkdir("C:\\InvoiceGenerator")
except:
    pass


trans = QTranslator() 

#it's header for invoice
class header:
    def __init__(self, Cust_Name,Comp_Name,Comp_Street,Comp_Zip,Comp_City,Comp_Country,Comp_Phone,InvoiceNr,Cust_Id,Cust_street,Cust_City):
        self.Comp_Name=Comp_Name
        self.Comp_Street=Comp_Street
        self.Comp_Zip=Comp_Zip
        self.Comp_City=Comp_City
        self.Comp_Country=Comp_Country
        self.Comp_Phone=Comp_Phone
        self.Customer_Name = Cust_Name
        self.Customer_Id = Cust_Id
        self.InvoiceNumber = InvoiceNr
        self.Cust_street=Cust_street
        self.Cust_City=Cust_City
        timedate = time.asctime()
        self.date = timedate[4:8] + timedate[8:10] + ", " + timedate[20:24] + "."
        self.time = " " + timedate[11:20]

class Buy_header:
    def __init__(self,Comp_Name,Comp_Street,Comp_Zip,Comp_City,Comp_Country,Comp_Phone):
        self.Comp_Name = Comp_Name
        x = date.today()
        self.date=x.strftime("%A, %d %B. %Y")
        self.Comp_Street = Comp_Street
        self.Comp_Zip = Comp_Zip
        self.Comp_City = Comp_City
        self.Comp_Country = Comp_Country
        self.Comp_Phone = Comp_Phone
# detail about each product
class product:
    def __init__(self, ItemId,quantity,productId,description, price, tax,netTotal,grossTotal):
        self.ItemId=ItemId
        self.quantity = quantity
        self.productId=productId
        self.description=description
        self.price = price
        self.tax = tax
        self.netTotal =netTotal
        self.grossTotal = grossTotal

class Buy_Product:
    def __init__(self,Artikelname, Menge, Ankaufspreis, Zwischensumme,total):
        self.Artikelname = Artikelname
        self.Menge = Menge
        self.Ankaufspreis = Ankaufspreis
        self.Zwischensumme = Zwischensumme
        self.total=total
# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        global helper
              
        helper = helper("invoice.db")

        last_language= load_last_language()
        load_message(last_language)        
        change_language(last_language, "MainWindow.ui", self)
      
    def refresh(self):
        #@Click #Show
        self.handle_menu()        
        self.handle_buttons() 
        self.clear_and_fill()
        
    def clear_and_fill(self):                       
        self.hide_all_group_box()
        self.DateEditInvoiceCreate.setDate(QDate.currentDate())
        self.dateEditSoldFrom.setDate(QDate.currentDate())
        self.dateEditSoldTo.setDate(QDate.currentDate())
        self.fill_customer_table()
        self.fill_product_table()  
        self.fill_invoice_table()
        self.fill_admin_own()
        self.clear_customer_fields()        
        self.clear_product_fields()
        self.clear_table_InvoiceItem()
        self.lineEditCustomerIdInvoice.clear()
        self.LineEditCustomerInvoiceCreate.clear()
        self.lineEditInvoiceNr.clear()
        self.LineEditProductID.clear()
        self.LineEditSubTotal.clear()
        self.LineEditGrossTotal.clear()
        self.LineEditQuantity.clear()
        self.CmbBoxTax.setCurrentIndex(0)
    
    def handle_buttons(self):
        
        self.stackedWidget.setCurrentIndex(3)       
        self.BtnInvoice.clicked.connect(lambda:  [self.stackedWidget.setCurrentIndex(0), self.clear_and_fill()])
        self.BtnBuy.clicked.connect(lambda:      [self.stackedWidget.setCurrentIndex(2), self.clear_and_fill()])        
        self.BtnCustomer.clicked.connect(lambda: [self.stackedWidget.setCurrentIndex(3), self.clear_and_fill()])
        self.BtnProduct.clicked.connect(lambda:  [self.stackedWidget.setCurrentIndex(4), self.clear_and_fill()])
        self.BtnReport.clicked.connect(lambda: [self.stackedWidget.setCurrentIndex(6)])
        self.BtnAdmin.clicked.connect(lambda:    [self.stackedWidget.setCurrentIndex(5), self.clear_and_fill()])
        #Edit
        self.BtnEditInvoice.clicked.connect(self.edit_invoice)
        self.BtnEditNewCustomer.clicked.connect(lambda: self.groupBoxCustomer.show())
        self.BtnEditNewProduct.clicked.connect(lambda:  self.frameProduct.show())
        #Create
        self.BtnCreateInvoice.clicked.connect(self.create_invoice)
        #Close
        self.BtnCloseInvoice.clicked.connect(lambda: [self.stackedWidget.setCurrentIndex(0), self.clear_and_fill()])
        self.BtnCloseCustomer.clicked.connect(lambda:  [self.groupBoxCustomer.hide(), self.clear_and_fill()])
        self.BtnCloseProduct.clicked.connect(lambda:  [self.frameProduct.hide(), self.clear_and_fill()])
        self.BtnCloseApp.clicked.connect(lambda:  self.close())
        #Save
        self.BtnSaveCustomer.clicked.connect(self.save_customer)
        self.BtnSaveInvoice.clicked.connect(self.save_invoice)
        self.BtnSaveProduct.clicked.connect(self.save_product)
        self.BtnSaveAdminOwn.clicked.connect(self.save_admin_own)
        #Delete
        self.BtnDeleteCustomer.clicked.connect(self.delete_customer)
        self.BtnDeleteItemInvoice.clicked.connect(self.delete_item_invoice)
        self.BtnDeleteProduct.clicked.connect(self.delete_product)
        self.BtnDeleteBuyItem.clicked.connect(self.delete_buy_item)
        #Clear
        self.BtnClearCustomerFields.clicked.connect(self.clear_customer_fields)
        self.BtnClearProductFields.clicked.connect(self.clear_product_fields)
        # print
        self.BtnPrintInvoice.clicked.connect(self.printinvoice)
        self.BtnPrintBuy.clicked.connect(self.save_buy) #(lambda: [self.save_buy(), self.printbuy()])
        self.BtnShowSaleReport.clicked.connect(self.show_sale_report)
        self.BtnShowStockReport.clicked.connect(self.show_stock_report)
        self.BtnShowBuyReport.clicked.connect(self.show_buy_report)
        #Filter
        #Combobox Filter by Paid/Unpaid
        self.CmbBoxStatusInvoice.view().pressed.connect(self.filter_by_status)
        self.BtnNoFilterInvoice.clicked.connect(self.filter_no_filter)
        
        #@Return
        self.LineEditProductID.returnPressed.connect(self.fill_item_line)  
        self.LineEditQuantity.returnPressed.connect(self.fill_item_line)  
        self.lineEditBuyPrice.returnPressed.connect(self.fill_item_buy_line)  
        self.lineEditBuyQuantity.returnPressed.connect(self.fill_item_buy_line)  
        # @Tableitem Clicked
        self.tableWidgetCustomer.clicked.connect(self.move_customer_fields)
        self.tableWidgetProduct.clicked.connect(self.move_product_fields)
    
    def handle_menu(self):        
        #@Menu Language change
        self.actionEnglish.triggered.connect(lambda: [load_message("english"), change_language("english","MainWindow.ui" , self),\
                                                      set_last_language("english")])
        self.actionDeutsch.triggered.connect(lambda: [load_message("deutsch"), change_language("deutsch","MainWindow.ui", self),\
                                                      set_last_language("deutsch")])        

    def hide_all_group_box(self):
        self.groupBoxCustomer.hide() 
        self.frameProduct.hide() 
          
 #@Save
    def save_customer(self):
        try:
            ci = self.lineEditCustomerId.text()
            fn = self.lineEditForename.text()
            ln = self.lineEditLastname.text()
            ac = self.lineEditAreaCode.text()
            st = self.lineEditStreet.text()
            cy = self.lineEditCity.text() 
            sta = self.lineEditState.text()
            na = self.lineEditNation.text()
            ds = self.plainTextEditNote.toPlainText()
            cust = (fn, ln, ac, st, cy, sta, na, ds)            
           
            if self.lineEditCustomerId.text():
                helper.edit("UPDATE customer SET ForeName=?, LastName=?, AreaCode=?, Street=?, City=?, State=?, Nation=?, Description=? WHERE CustomerId="+ci,cust)
            else: 
                helper.insert("INSERT INTO customer (ForeName, LastName, AreaCode, Street, City, State, Nation, Description) Values(?,?,?,?,?,?,?,?)",cust)
            self.clear_customer_fields()
            self.fill_customer_table()
            self.statusBar().showMessage(messageText[1][0],5000) 
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))              
    def save_admin_own(self):
        try:
            cn = self.lineEditAdminCompanyName.text()
            cs = self.lineEditAdminCompanyStreet.text()
            cz = self.lineEditAdminCompanyZip.text()
            cc = self.lineEditAdminCompanyCity.text()
            cna = self.lineEditAdminCompanyNation.text()
            ct = self.lineEditAdminCompanyTelefon.text()         
            ce = self.lineEditAdminCompanyEmail.text()
            own = (cn, cs, cz, cc, cna, ct, ce)          
            ci = '1'
            helper.edit("UPDATE OwnCompany SET OwnName=?, OwnStreet=?, OwnZip=?, OwnCity =?, OwnNation=?, OwnTelefon=?, OwnEmail=? WHERE OwnCompanyId="+ci,own)
            self.statusBar().showMessage(messageText[2][0],5000)
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))              

    def save_product(self):
        try:
            pi = self.lineEditProductId.text()
            pd = self.lineEditProductDescription.text()
            pQuantity = self.LineEditProductQuantity.text()            
            pp = self.lineEditProductBuyPrice.text()
            sp = self.lineEditProductSalesPrice.text()
            pro = (pd, pQuantity, pp, sp)
            if self.lineEditProductId.text():
                helper.edit("UPDATE product SET Description=?, quantity=?, BuyPrice=?, SellPrice=?  WHERE ProductId="+pi, pro)
            else: 
                helper.insert("INSERT INTO product (Description, Quantity, BuyPrice, SellPrice ) Values(?,?,?,?);", pro)
            self.clear_product_fields()
            self.fill_product_table()
            self.statusBar().showMessage(messageText[0][0], 5000)
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))              
        
    def save_invoice(self):
# Update invoice
        try: 
            cn = self.lineEditCustomerIdInvoice.text()        
            invnr = self.lineEditInvoiceNr.text()
            pu = self.CmbBoxPaidUnpaid.currentText()
            invo = (cn, pu)    
            helper.edit("Update invoice set CustomerId=?, PaidUnpaid=? WHERE InvoiceId="+invnr,invo)             
            self.statusBar().showMessage(messageText[3][0],5000) 
            self.fill_invoice_table()
            self.fill_invoice_item_table(invnr)
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))       
    
    def save_buy(self):
        try:
            if self.tableWidgetBuyItem.rowCount() > 0:
                andat = date.today()
                helper.insert("INSERT INTO Ankauf (Ankaufdatum) VALUES (?)",(str(andat),))
                ankauf = helper.select("SELECT * FROM Ankauf ORDER BY AnkaufId DESC LIMIT 1;")
                
                  
                len = self.tableWidgetBuyItem.rowCount()
                for row in range(len):
                    product_desc = self.tableWidgetBuyItem.item(row, 0).text()
                    product_quantity = int(self.tableWidgetBuyItem.item(row, 1).text())
                    product_price = float(self.tableWidgetBuyItem.item(row, 2).text())
                    
                    helper.insert("INSERT INTO Product (Description,quantity, BuyPrice) VALUES (?, ?, ?)",(product_desc, product_quantity,product_price))
        
                    product = helper.select("SELECT * FROM Product ORDER BY ProductId DESC LIMIT 1")
        
                    helper.insert("INSERT INTO AnkaufDetail (AnkaufId, ProductId, AnkaufMenge, AnkaufPreis) VALUES (?,?,?,?)",(ankauf[0][0], product[0][0], product_quantity, product_price))
        
                self.fill_product_table()
                self.clear_table_buy()
                self.statusBar().showMessage(messageText[4][0],5000)   
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
        
    def getData(self, column_list, table: QTableWidget): # -> List[Tuple[str]]:
        try:
            """Fetch the data from the QTableWidget and return it as `data`."""
            data = []
            for row in range(table.rowCount()):
                rowData = []
                for col in column_list:
                    if table.item(row, col):
                        rowData.append(table.item(row, col).data(Qt.EditRole))
                    
                data.append(tuple(rowData))
            return data  
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  

#@Clear
    def clear_customer_fields(self):
        self.lineEditCustomerId.clear()
        self.lineEditForename.clear()
        self.lineEditLastname.clear()
        self.lineEditAreaCode.clear()
        self.lineEditStreet.clear()
        self.lineEditCity.clear() 
        self.lineEditState.clear()
        self.lineEditNation.clear()
        self.plainTextEditNote.clear()
    def clear_product_fields(self):
        self.lineEditProductId.clear()
        self.LineEditProductQuantity.clear()
        self.lineEditProductDescription.clear()
        self.lineEditProductBuyPrice.clear() 
        self.lineEditProductSalesPrice.clear() 
        
    def clear_buy_fields(self):
        self.lineEditBuyProductName.clear()
        self.lineEditBuyQuantity.clear()
        self.lineEditBuyPrice.clear() 
    def clear_table_InvoiceItem(self):
        self.tableWidgetInvoiceItem.setRowCount(0)  
    def clear_table_buy(self):
        self.tableWidgetBuyItem.setRowCount(0)                             
#@Fill    
    def fill_item_line(self):
        try:
            val = self.LineEditQuantity.text()
            if(len(val) == 1):
                amount = int(re.search(r'\d+', val).group())
            elif(len(val) > 1):
                amount = int(val)
# update product quantity    
            if self.LineEditProductID.text():
                EnProductId = self.LineEditProductID.text()
                data = helper.select(f"Select ProductId, Description, SellPrice, Quantity from Product where ProductId= {EnProductId}")
                if data:
                    if(amount > int(data[0][3])):
                        QMessageBox.warning(self, 'Error', messageText[14][0] + f"{data[0][3]}", QMessageBox.Ok)
                        self.LineEditQuantity.setFocus()
                        return
                else:
                    QMessageBox.warning(self, 'Error', messageText[8][0], QMessageBox.Ok) #Product not found
                    return
                if not data[0][2]:
                    QMessageBox.warning(self, 'Error', messageText[17][0], QMessageBox.Ok)
                    return
                
                quantity_new = int(data[0][3]) - amount
                helper.edit(f"UPDATE Product SET quantity=? where ProductId= {EnProductId}", (quantity_new,))
 # insert invoice item
                invnr = self.lineEditInvoiceNr.text()
                qua = amount
                pid = EnProductId
                pri = data[0][2]
                tax = self.CmbBoxTax.currentText()
                res = (invnr, qua, pid, pri, tax)
        
                helper.insert("INSERT INTO InvoiceItem (InvoiceId, Quantity, ProductId, SellPrice, Tax) VALUES (?, ?, ?, ?, ?)", res)
                invitemnr_que = helper.select("select max(InvoiceId) from Invoice")
                invitemnr = invitemnr_que[0][0]
                for row, form in enumerate(data):
                    row_position = self.tableWidgetInvoiceItem.rowCount()
                    self.tableWidgetInvoiceItem.insertRow(row_position)
                    self.tableWidgetInvoiceItem.setItem(row_position, 0,QTableWidgetItem(str(invitemnr)))
                    for column, item in enumerate(form):
                        self.tableWidgetInvoiceItem.setItem(row_position, 1,
                                                            QTableWidgetItem(str(self.LineEditQuantity.text())))
                        self.tableWidgetInvoiceItem.setItem(row_position, column + 2,
                                                            QTableWidgetItem(str(item)))  # ProductId
                        self.tableWidgetInvoiceItem.setItem(row_position, column + 3,
                                                            QTableWidgetItem(str(item)))  # ProductDescription
                        self.tableWidgetInvoiceItem.setItem(row_position, column + 4,
                                                            QTableWidgetItem(str(item)))  # SellPrice
                        self.tableWidgetInvoiceItem.setItem(row_position, 5, QTableWidgetItem(
                            str(self.CmbBoxTax.currentText())))  # Tax
                price = data[0][2]
                nettotal = (price * int(self.LineEditQuantity.text()))
                round(nettotal, 2)
                if self.CmbBoxTax.currentText() == 0:
                    grosstotal = nettotal
                else:
                    tax = Decimal(self.CmbBoxTax.currentText())
                    grosstotal = Decimal(nettotal) * ((tax / 100) + 1)
                    grosstotal = float(grosstotal)
    
                self.tableWidgetInvoiceItem.setItem(row_position, 6, QTableWidgetItem(str(nettotal)))
                self.tableWidgetInvoiceItem.setItem(row_position, 7, QTableWidgetItem(str("{:.2f}".format(grosstotal))))
    
                self.LineEditProductID.clear()
                self.LineEditQuantity.clear()
                col5sum = 0
                col6sum = 0
                rowCount = self.tableWidgetInvoiceItem.rowCount()
                for row in range(rowCount):
                    col5sum += Decimal(self.tableWidgetInvoiceItem.item(row, 6).text())
                    col6sum += Decimal(self.tableWidgetInvoiceItem.item(row, 7).text())
                self.LineEditSubTotal.setText(str(col5sum))
                self.LineEditGrossTotal.setText(str(col6sum))
                self.LineEditQuantity.setFocus()
            else:
                QMessageBox.warning(self, 'Error', messageText[9][0], QMessageBox.Ok)
        except Exception as e:
                ErrorLogger.WriteError(traceback.format_exc())
                QMessageBox.critical(None, 'Exception raised', format(e))                       

    def fill_item_buy_line(self):
        try:
            if self.lineEditBuyQuantity.text() and self.lineEditBuyPrice.text():
                row_position = self.tableWidgetBuyItem.rowCount()
                self.tableWidgetBuyItem.insertRow(row_position)
                self.tableWidgetBuyItem.setItem(row_position, 0, QTableWidgetItem(str(self.lineEditBuyProductName.text())))
                self.tableWidgetBuyItem.setItem(row_position, 1, QTableWidgetItem(str(self.lineEditBuyQuantity.text())))
                self.tableWidgetBuyItem.setItem(row_position, 2, QTableWidgetItem(str(self.lineEditBuyPrice.text())))
                zwischensumme = int(self.lineEditBuyQuantity.text()) * int(self.lineEditBuyPrice.text())
                self.tableWidgetBuyItem.setItem(row_position, 3, QTableWidgetItem(str(zwischensumme)))
                self.clear_buy_fields()
                self.lineEditBuyProductName.setFocus()
            else:
                QMessageBox.warning(self, 'Info', messageText[15][0], QMessageBox.Ok)
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))
        
        
    def fill_customer_table(self):
        data = helper.select("select * from Customer")        
        self.fill_my_table(self.tableWidgetCustomer, data)
    def fill_product_table(self):

        data = helper.select("select ProductId, Description, quantity, BuyPrice, SellPrice from Product")
        self.fill_my_table(self.tableWidgetProduct, data)

    def fill_invoice_table(self):
        self.tableWidgetInvoice.setRowCount(0)        
        data = helper.select("select * from InvoiceCustomer")
        for row, form in enumerate(data):
            row_position = self.tableWidgetInvoice.rowCount()
            self.tableWidgetInvoice.insertRow(row_position)  
            for column, item in enumerate(form):
                if item:
                    self.tableWidgetInvoice.setItem(row, column, QTableWidgetItem(str(item)))    
    def fill_invoice_item_table(self, invnr):   
        data = helper.select("select ItemId from InvoiceItem where InvoiceId="+invnr)
        for row, form in enumerate(data):
            for i, item in enumerate(form):
                    if item:
                        self.tableWidgetInvoiceItem.setItem(row, 0, QTableWidgetItem(str(item)))  
    def fill_admin_own(self):
        data = helper.select("select * from OwnCompany")
        if data:
            result = data.pop()
            self.lineEditAdminCompanyName.setText(result[1])
            self.lineEditAdminCompanyStreet.setText(result[2])
            self.lineEditAdminCompanyZip.setText(result[3])
            self.lineEditAdminCompanyCity.setText(result[4])
            self.lineEditAdminCompanyNation.setText(result[5])
            self.lineEditAdminCompanyTelefon.setText(result[6])         
            self.lineEditAdminCompanyEmail.setText(result[7])
    
    def fill_my_table(self, table = QTableWidget, data=[]):   
        table.setRowCount(0)        
        for row, form in enumerate(data):
            row_position = table.rowCount()
            table.insertRow(row_position)  
            for column, item in enumerate(form):
                if item:
                    table.setItem(row, column, QTableWidgetItem(str(item)))            
                    
#@Delete
    def delete_customer(self):
        try:
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),0):
                customerid = self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),0).text()
                helper.delete("DELETE FROM Customer WHERE CustomerId =" + customerid)
                self.fill_customer_table()
                self.statusBar().showMessage(messageText[5][0],5000) 
            else:
                QMessageBox.warning(self, 'Info', messageText[10][0], QMessageBox.Ok) 
            self.clear_customer_fields()
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
            
    def delete_item_invoice(self):
        try:
            if self.tableWidgetInvoiceItem.currentRow:
            # if self.tableWidgetInvoiceItem.item(self.tableWidgetInvoiceItem.currentRow(),1):
                EnProductId = (self.tableWidgetInvoiceItem.item(self.tableWidgetInvoiceItem.currentRow(),2).text())
                data = helper.select(f"Select ProductId, Description, Quantity, SellPrice from Product where ProductId= {EnProductId}")
                amount = int(data[0][3])
                item_quantity = int(self.tableWidgetInvoiceItem.item(self.tableWidgetInvoiceItem.currentRow(),1).text())
                quantity_new =  item_quantity + amount
                helper.edit(f"UPDATE Product SET quantity=? where ProductId= {EnProductId}", (quantity_new,))            
                itemid = self.tableWidgetInvoiceItem.item(self.tableWidgetInvoiceItem.currentRow(),0).text()
                helper.delete("DELETE FROM InvoiceItem WHERE ItemId ="+itemid)
                self.tableWidgetInvoiceItem.removeRow(self.tableWidgetInvoiceItem.currentRow())
                self.statusBar().showMessage(messageText[6][0],5000) 
            else:
                QMessageBox.warning(self, 'Info', messageText[16][0], QMessageBox.Ok) 
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))       

    def delete_buy_item(self):
        try:
            if self.tableWidgetBuyItem.selectionModel().hasSelection():
                self.tableWidgetBuyItem.removeRow(self.tableWidgetBuyItem.currentRow())
                self.statusBar().showMessage(messageText[6][0],5000)
            else:
                QMessageBox.warning(self, 'Info', messageText[12][0], QMessageBox.Ok)    
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
        
    def delete_product(self):
        try:
            if self.tableWidgetProduct.selectionModel().hasSelection():
                Productid = self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),0).text()
                helper.delete("DELETE FROM Product WHERE ProductId =" + Productid)
                self.fill_product_table()
                self.statusBar().showMessage(messageText[7][0],5000) 
            else:
                QMessageBox.warning(self, 'Info', messageText[12][0], QMessageBox.Ok)            
            self.clear_product_fields()            
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
            
#@Create
    def create_invoice(self):
        try:
            if self.tableWidgetCustomer.currentRow() >=0:
                try:
                    self.stackedWidget.setCurrentIndex(1)
                    invd = self.DateEditInvoiceCreate.date().toPyDate() 
                    helper.insert("insert into invoice (InvoiceDate) Values(?)",(invd,)) 
    
                    invnr_que = helper.select("select max(InvoiceId) from Invoice")
                    invnr = invnr_que[0][0]
                       
                    self.LineEditCustomerInvoiceCreate.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),1).text() 
                                                               + ' ' + self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),2).text())
                    self.lineEditCustomerIdInvoice.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),0).text())
                    self.lineEditInvoiceNr.setText(str(invnr))
                    self.LineEditQuantity.setFocus()
                except Exception as e:
                    ErrorLogger.WriteError(traceback.format_exc())
                    QMessageBox.critical(None, 'Exception raised', format(e))       
                            
            else:
                QMessageBox.warning(self, 'Info', messageText[10][0], QMessageBox.Ok)
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
                
#@Edit
    def edit_invoice(self):
        try:
            if self.tableWidgetInvoice.currentRow() >=0:
                self.stackedWidget.setCurrentIndex(1)
                self.LineEditCustomerInvoiceCreate.setText(self.tableWidgetInvoice.item(self.tableWidgetInvoice.currentRow(),3).text() 
                                                           + ' ' + self.tableWidgetInvoice.item(self.tableWidgetInvoice.currentRow(),4).text())
                self.lineEditCustomerIdInvoice.setText(self.tableWidgetInvoice.item(self.tableWidgetInvoice.currentRow(),2).text())
        # Get the invoice number
                invnr = self.tableWidgetInvoice.item(self.tableWidgetInvoice.currentRow(),0).text()
                self.lineEditInvoiceNr.setText(invnr)
        # fill InvoiceItem            
                self.tableWidgetInvoiceItem.setRowCount(0)        
                data = helper.select("select ItemId, Quantity, ProductId, Description,SellPrice, Tax from InvoiceItemProduct where InvoiceId="+invnr)
                for row, form in enumerate(data):
                    row_position = self.tableWidgetInvoiceItem.rowCount()
                    self.tableWidgetInvoiceItem.insertRow(row_position)  
                    for column, item in enumerate(form):
                        if item:
                            self.tableWidgetInvoiceItem.setItem(row, column, QTableWidgetItem(str(item)))  
                column_list = [1,4,5]            
                itemdata = self.getData(column_list, self.tableWidgetInvoiceItem)
                for row , form in enumerate(data):
                        quantity = int(form[1])
                        price = Decimal(form[4])
                        tax = Decimal(form[5])
                        nettotal = quantity * price
                        grosstotal = nettotal * (tax / 100 + 1)
                        grosstotal = float(grosstotal)
                        self.tableWidgetInvoiceItem.setItem(row, 6, QTableWidgetItem(str(nettotal)))
                        self.tableWidgetInvoiceItem.setItem(row, 7, QTableWidgetItem(str("{:.2f}".format(grosstotal))))     
                col5sum=0
                col6sum=0
                rowCount = self.tableWidgetInvoiceItem.rowCount()
                for row in range(rowCount):
                    col5sum+=Decimal(self.tableWidgetInvoiceItem.item(row,6).text())
                    col6sum+=Decimal(self.tableWidgetInvoiceItem.item(row,7).text())
                self.LineEditSubTotal.setText(str(col5sum))
                self.LineEditGrossTotal.setText(str(col6sum))                    
            
            else:
                QMessageBox.warning(self, 'Info', messageText[11][0], QMessageBox.Ok)  
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
                                  
#@Move
    def move_customer_fields(self):
            self.clear_customer_fields()
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),0):
                self.lineEditCustomerId.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),0).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),1):
                self.lineEditForename.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),1).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),2):
                self.lineEditLastname.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),2).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),3):
                self.lineEditAreaCode.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),3).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),4):
                self.lineEditStreet.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),4).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),5):
                self.lineEditCity.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),5).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),6):
                self.lineEditState.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),6).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),7):
                self.lineEditNation.setText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),7).text())        
            if self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),8):
                self.plainTextEditNote.setPlainText(self.tableWidgetCustomer.item(self.tableWidgetCustomer.currentRow(),8).text()) 
    def move_product_fields(self):
            self.clear_product_fields()
            if self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),0):
                self.lineEditProductId.setText(self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),0).text())        
            if self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),1):
                self.lineEditProductDescription.setText(self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),1).text())  
            if self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),2):   
                self.LineEditProductQuantity.setText(self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),2).text())        
            if self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),3):   
                self.lineEditProductBuyPrice.setText(self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),3).text())        
            if self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),4):   
                self.lineEditProductSalesPrice.setText(self.tableWidgetProduct.item(self.tableWidgetProduct.currentRow(),4).text())        
#invoice printing
    def printinvoice(self):
        try:
            self.save_invoice()
            self.tableWidgetCustomer.setRowCount(0)
            #retrive own company data
            data = helper.select("select * from OwnCompany")
            Comp_Name=data[0][1]
            Comp_Street=data[0][2]
            Comp_Zip=data[0][3]
            Comp_City=data[0][4]
            Comp_Country=data[0][5]
            Comp_Phone=data[0][6]
            # Customer Name
            Cust_Name = self.LineEditCustomerInvoiceCreate.text()
            # Invoice number
            InvoiceNr = self.lineEditInvoiceNr.text()
            #Customer id
            Cust_Id=self.lineEditCustomerIdInvoice.text()
            #retrive customer data on the base of id
            Cust_data = helper.select("select * from Customer where CustomerId=" + Cust_Id)
            Cust_street=Cust_data[0][4]
            Cust_City=Cust_data[0][5]
    
            rows=self.tableWidgetInvoiceItem.rowCount()
            r=0 #r stands for single row
            head = header(Cust_Name,Comp_Name,Comp_Street,Comp_Zip,Comp_City,Comp_Country,Comp_Phone,InvoiceNr,Cust_Id,Cust_street,Cust_City)
            pdf = canvas.Canvas("C:\\InvoiceGenerator\\" + str(int(head.InvoiceNumber)) + ".pdf")
            pdfgen.header(head, pdf)
            pdfgen.middle(pdf)
            ycooridinate = 600
            total=0
            Net_Total=0
            while r < rows:
                if self.tableWidgetInvoiceItem.item(r, 0):
                    itemId = self.tableWidgetInvoiceItem.item(r, 0).text()
                if self.tableWidgetInvoiceItem.item(r, 1):
                    quantity = self.tableWidgetInvoiceItem.item(r, 1).text()
                if self.tableWidgetInvoiceItem.item(r, 2):    
                    productId = self.tableWidgetInvoiceItem.item(r, 2).text()
                if self.tableWidgetInvoiceItem.item(r, 3):
                    description = self.tableWidgetInvoiceItem.item(r, 3).text()
                if self.tableWidgetInvoiceItem.item(r, 4):    
                    price = self.tableWidgetInvoiceItem.item(r, 4).text()
                if (self.tableWidgetInvoiceItem.item(r, 5)) is not None :
                    tax = self.tableWidgetInvoiceItem.item(r, 5).text()
                else:
                    tax = ''
                if self.tableWidgetInvoiceItem.item(r, 6):
                    netTotal = self.tableWidgetInvoiceItem.item(r, 6).text()
                if self.tableWidgetInvoiceItem.item(r, 7):
                    grossTotal = self.tableWidgetInvoiceItem.item(r, 7).text()
                
                total=total+float(grossTotal)
                Net_Total=Net_Total+float(netTotal)
                # currproduct = product(Data[0], Data[1], Data[2], Data[3], Data[4], Data[5], Data[6])
                currproduct = product(itemId,quantity,productId,description,price,tax,netTotal,grossTotal)
                r = r + 1
                pdf.drawString(50, ycooridinate, itemId)
                pdf.drawString(105, ycooridinate, quantity)
                pdf.drawString(170, ycooridinate, productId)
                pdf.drawString(330, ycooridinate, price)
                pdf.drawString(390, ycooridinate, tax)
                pdf.drawString(450, ycooridinate, netTotal)
                pdf.drawString(520, ycooridinate, grossTotal)
                pdf.setFont("Courier-Bold", 9)
                ycooridinate = pdfgen.additem(currproduct, pdf, ycooridinate)
            pdf.setFont("Courier-Bold", 11)
            pdfgen.footer(pdf, total, Net_Total,ycooridinate)
            pdf.save()
            file_path = "C:\\InvoiceGenerator\\" + str(int(head.InvoiceNumber)) + ".pdf"
            # print the document
            os.startfile(file_path, 'print')
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
    def show_stock_report(self):
        try:
            data = helper.select("select * from Product where Quantity !='' and Quantity > 0")
            # print(data)
            # Stock report
            report = reportObj("stock", data)
            report.generate_stock_report("stockReport.pdf")

        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  

    def show_buy_report(self):
        try:
            buy_date_from = self.dateEditSoldFrom.date().toPyDate()
            buy_date_to   = self.dateEditSoldTo.date().toPyDate()
            data = helper.select(f"select * from BuyReport where Ankaufdatum between '{buy_date_from}' and '{buy_date_to}'")
            # print(data)
            # create a Buy Report 
            report = reportObj("buy", data, buy_date_from, buy_date_to)
            report.generate_buy_report("buyReport.pdf")


        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  

    def show_sale_report(self):
        try:
            sold_date_from = self.dateEditSoldFrom.date().toPyDate()
            sold_date_to   = self.dateEditSoldTo.date().toPyDate()
            data = helper.select(f"select * from SalesReport where InvoiceDate between '{sold_date_from}' and '{sold_date_to}'")
            # print(data)
            # create a salesReport object and pass the data to it
            report = reportObj("sales", data, sold_date_from, sold_date_to)
            report.generate_sales_report("salesReport.pdf")
            
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
    
    def printbuy(self):
        try:
            if self.tableWidgetBuyItem.rowCount() > 0:
                rows = self.tableWidgetBuyItem.rowCount()
                r = 0  # r stands for single row
                data = helper.select("select * from OwnCompany")
                Comp_Name=data[0][1]
                Comp_Street = data[0][2]
                Comp_Zip = data[0][3]
                Comp_City = data[0][4]
                Comp_Country = data[0][5]
                Comp_Phone = data[0][6]
                head = Buy_header(Comp_Name,Comp_Street, Comp_Zip, Comp_City, Comp_Country, Comp_Phone)
                pdf = canvas.Canvas("C:\\InvoiceGenerator\\" + str(head.date) + ".pdf")
                purchase.header(head, pdf)
                purchase.middle(pdf)
                ycooridinate = 670
                total = 0
                while r < rows:
                    Artikelname = self.tableWidgetBuyItem.item(r, 0).text()
                    Menge = self.tableWidgetBuyItem.item(r, 1).text()
                    Ankaufspreis = self.tableWidgetBuyItem.item(r, 2).text()
                    Zwischensumme = self.tableWidgetBuyItem.item(r, 3).text()
                    total=total+float(Zwischensumme)
                    currproduct = Buy_Product(Artikelname, Menge, Ankaufspreis, Zwischensumme,total)
                    r = r + 1
                    pdf.drawString(350, ycooridinate, Menge)
                    pdf.drawString(410, ycooridinate, Ankaufspreis)
                    pdf.drawString(500, ycooridinate, Zwischensumme)
                    pdf.setFont("Courier-Bold", 9)
                    ycooridinate = purchase.additem(currproduct, pdf, ycooridinate)
                pdf.setFont("Courier-Bold", 11)
                purchase.footer(total,pdf)
                pdf.save()
                file_path = "C:\\InvoiceGenerator\\" + str(head.date) + ".pdf"
                #print the document
                os.startfile(file_path, 'print')
                self.clear_table_buy() 
            else:
                QMessageBox.warning(self, 'Info', messageText[13][0], QMessageBox.Ok)
        except Exception as e:
            ErrorLogger.WriteError(traceback.format_exc())
            QMessageBox.critical(None, 'Exception raised', format(e))                  
                           
#@Filter
    def filter_by_status(self, index):
        text = self.CmbBoxStatusInvoice.model().itemFromIndex(index)
        text = text.text()
        data = helper.select(f"select * from InvoiceCustomer where PaidUnpaid= '{text}'")
        self.tableWidgetInvoice.setRowCount(0)
        for row, form in enumerate(data):
            row_position = self.tableWidgetInvoice.rowCount()
            self.tableWidgetInvoice.insertRow(row_position)  
            for column, item in enumerate(form):
                if item:
                    self.tableWidgetInvoice.setItem(row, column, QTableWidgetItem(str(item)))  
    def filter_no_filter(self):
        data = helper.select("select * from InvoiceCustomer")
        self.tableWidgetInvoice.setRowCount(0)
        for row, form in enumerate(data):
            row_position = self.tableWidgetInvoice.rowCount()
            self.tableWidgetInvoice.insertRow(row_position)  
            for column, item in enumerate(form):
                if item:
                    self.tableWidgetInvoice.setItem(row, column, QTableWidgetItem(str(item)))          
                    
#@Language
def load_last_language():
    try:
        language_file = open(r"last_language.txt", "r+")
        last_language = language_file.readline()
        language_file.close()  
        return last_language                 
    except Exception as e:
        ErrorLogger.WriteError(traceback.format_exc())
        QMessageBox.critical(None, 'Exception raised', format(e))                  

def set_last_language(language):
    try:
        language_file = open(r"last_language.txt", "w")
        language_file.write(language)
        language_file.close()      
    except Exception as e:
        ErrorLogger.WriteError(traceback.format_exc())
        QMessageBox.critical(None, 'Exception raised', format(e))                  
    
def load_message(language):
    try:
        global messageText
        messageText = helper.select(f"Select text from messagetext where language like '{language}' order by messageid")  
    except Exception as e:
        ErrorLogger.WriteError(traceback.format_exc())
        QMessageBox.critical(None, 'Exception raised', format(e))                  

def change_language(language, callingWindow, callingClass):
    try:
        if language:
            trans.load(language)
            QApplication.instance().installTranslator(trans)
            uic.loadUi(callingWindow, callingClass)
            callingClass.refresh()            
        else:
            QApplication.instance().removeTranslator(trans) 
    except Exception as e:
        ErrorLogger.WriteError(traceback.format_exc())
        QMessageBox.critical(None, 'Exception raised', format(e))                  


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())        
