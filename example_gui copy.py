#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

try:
    import wx
    import wx.grid as gridlib
    import datetime
    import calendar
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"


class baranunit(wx.Frame):

    def __init__(self, parent, title):
        """Constructor"""
        wx.Frame.__init__(self, parent=parent, title=title, size=(850, 400))
        panel = wx.Panel(self)
        myGrid = gridlib.Grid(panel)
        myGrid.CreateGrid(120, 9)
        self.initialize_grid(myGrid)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(myGrid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        self.Show(True)


    def initialize_grid(self, myGrid):
        #initialize the grid
        myGrid.SetColLabelValue(0, "Isim")
        myGrid.SetColLabelValue(1, "Soy Isim")
        myGrid.SetColLabelValue(2, "Ay - Yil")
        myGrid.SetColLabelValue(3, "Odeme Tarihi")
        myGrid.SetColLabelValue(4, "Odeme Sekli")
        myGrid.SetColLabelValue(5, "Miktar")
        myGrid.SetColLabelValue(6, "Tel no:")
        myGrid.SetColLabelValue(7, "Kefil Isim")
        myGrid.SetColLabelValue(8, "Kefil Tel no:")
        
        current_month = datetime.datetime.now()
        row_num = self.populate_table_with_entered_info(myGrid)
        
        for i in range(myGrid.GetNumberRows()):
            #the column we are interested in is "Ay-Yil"
            myGrid.SetCellValue(i, 3, current_month.strftime("%Y-%m"))
            #add one to month
            current_month = self.add_months(current_month , 1 )

    def add_months(self, sourcedate,months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return datetime.date(year,month,day)

    def populate_table_with_entered_info(self, myGrid):
        pass
        #establish connection to mysql

        #look up data and populate


class baranblock(wx.Frame):
    
    def __init__(self, parent, title):
        """Constructor"""
        wx.Frame.__init__(self, parent=parent, title=title)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        sizer = wx.GridBagSizer(10, 10)
        counter = 1;
        for i in range(0, 3):
            for j in range(0, 7):
                #place baranblock objects on canvas
                block_name = "APT %d" % counter
                cur_block = wx.Button(self, -1, block_name)
                sizer.Add(cur_block, (j, i), flag=wx.ALL, border = 3)
                self.Bind(wx.EVT_BUTTON, self.updateRentInfo, cur_block)
                counter += 1
        self.SetSizerAndFit(sizer)
        self.SetSizeHints(-1,self.GetSize().y,-1,self.GetSize().y );
        self.Show(True)

    def updateRentInfo( self, event):
        #either ask whether we want to enter a new renter to the system or update an existing renter
        button_id = event.GetId()
        button_by_id = self.FindWindowById(button_id)
        self.popRentWindow( button_by_id )
    
    def popRentWindow( self, button_by_id):
        create_obj = True
        for child in self.GetChildren():
            if isinstance(child, baranunit) and child.GetTitle() == (self.GetTitle() + ' ' + button_by_id.GetLabel()):
                create_obj= False
                break
        if create_obj:
            apt_title = self.GetTitle() + ' ' + button_by_id.GetLabel()
            current_unit = baranunit(self, apt_title)        
            
    
class simpleapp_wx(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        self.children = [];
        self.initialize()
        

    def initialize(self):
        sizer = wx.GridBagSizer(50, 50)

        counter = 1;
        for i in range(0, 2):
            for j in range(0, 3):
                #place baranblock objects on canvas
                block_name = "Block %d" % counter
                cur_block = wx.Button(self, -1, block_name)
                sizer.Add(cur_block, (j, i), flag=wx.ALL, border = 10)
                self.Bind(wx.EVT_BUTTON, self.CreateBlock, cur_block)
                counter += 1
                
        

        self.SetSizerAndFit(sizer)
        self.SetSizeHints(-1,self.GetSize().y,-1,self.GetSize().y );
        self.Show(True)

    def CreateBlock(self,event):

        #when the button is clicked, we need to open another wxframe where we list the renters
        #dont re-create a block if the window is open for it and the user wants to re-open that windown
        #by clicking the block number
        button_id = event.GetId()
        button_by_id = self.FindWindowById(button_id)
 
        #if among the children there is a window with the button id, that                
        create_obj = True
        for child in self.GetChildren():
            #find the baranblock objects and see whether they were instantiated
            if isinstance(child, baranblock) and child.GetTitle() == button_by_id.GetLabel():
                create_obj= False
                break
        if create_obj:
            current_block = baranblock(parent=self, title=button_by_id.GetLabel())
        


if __name__ == "__main__":
    app = wx.App()
    frame = simpleapp_wx(None,-1,'baran development complex')
    app.MainLoop()
