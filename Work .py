import wx
import wx.grid
import sqlite3 as db
import datetime
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

class StartFrame(wx.Frame):#создание класса окна, в ктором и будут элементы интерфейса

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(190, 260))
        self.panel = wx.Panel(self)
        self.button1 = wx.Button(self.panel, id=-1, label="Создать пользователя", pos=(10, 10), size=(150, 100), style=0)
        self.button2 = wx.Button(self.panel, id=-1, label="Загрузить пользователя", pos=(10, 110), size=(150, 100), style=0)
        self.Bind(wx.EVT_BUTTON, self.CreatePolz, self.button1)
       # self.Bind(wx.EVT_BUTTON, self.Loading, self.button2)
    def CreatePolz(self,event):
        dlg = wx.TextEntryDialog(None, "Введите имя пользователя","Создание нового пользователя", "Первый")
        if dlg.ShowModal() == wx.ID_OK:
            self.response = dlg.GetValue()
        self.c=db.connect(database=self.response)#Добавить проверку на совпадения с прошлыми пользователями
        app.namepol=self.response
        self.cur = self.c.cursor()
        self.cur.execute("""create table if not exists workman (name TEXT,opisanie TEXT);""")
        self.c.commit()
        self.cur.execute("""create table if not exists Izdeliya
         (name TEXT,value INTEGER);""")
        self.c.commit()
        cur1.execute("INSERT INTO Profili(name) VALUES ('%s')"%(app.namepol))
        c1.commit()
        self.cur.close()
        self.c.close()
        app.CreateFrameGrid()


   # def Loading(self,event):


class AddFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(300, 480))
        self.panel = wx.Panel(self)
        self.label1 = wx.StaticText(self.panel, -1, "Введите  дату, день, месяц, год", (5, 0))
        self.Text1 = wx.TextCtrl(self.panel, -1, "12", pos=(5,15), size=(20, 20))
        self.Text2 = wx.TextCtrl(self.panel, -1, "7", pos=(30, 15), size=(20, 20))
        self.Text3 = wx.TextCtrl(self.panel, -1, "2018", pos=(55, 15), size=(40, 20))
        self.workman1=[]
        self.izd = []
        self.label2 = wx.StaticText(self.panel, -1, "Выберите рабочего", (5, 38))
        self.listBox1 = wx.ListBox(self.panel, -1, (5, 55), (270, 120), [], wx.LB_SINGLE)
        self.label2 = wx.StaticText(self.panel, -1, "Выберите изделие", (5, 175))
        self.listBox2 = wx.ListBox(self.panel, -1, (5, 195), (270, 120), [], wx.LB_SINGLE)
        self.label3 = wx.StaticText(self.panel, -1, "Введите количество изделий ", (5, 320))
        self.Text4 = wx.TextCtrl(self.panel, -1, "12", pos=(5,345), size=(40, 20))
        self.button1 = wx.Button(self.panel, id=-1, label="Добавить", pos=(5, 370), size=(70, 40),style=0)
        self.button2 = wx.Button(self.panel, id=-1, label="Отмена", pos=(80, 370), size=(70, 40), style=0)
        self.Workman()
        self.Izdeliya()
        self.Bind(wx.EVT_BUTTON, self.Add, self.button1)

    def Add(self,event):
        self.c = db.connect(database=app.namepol)
        self.cur = self.c.cursor()
        self.data=datetime.date(int(self.Text3.GetValue()),int(self.Text2.GetValue()),int(self.Text1.GetValue()))
        self.name=self.listBox1.GetString(self.listBox1.GetSelection())
        self.countnum="i"+str(self.listBox1.GetSelection())
        self.count = int(self.Text4.GetValue())
        self.cur.execute("INSERT INTO DataBase (Date,name,'%s') values  ('%s','%s','%i')" %
                         (self.countnum,self.data,self.name,self.count))
        self.c.commit()
        #добавить обработку сетки,разводку на есть в базе, нет в базе
        self.c.close()

    def Workman(self):
        self.c = db.connect(database=app.namepol)
        self.cur = self.c.cursor()
        self.cur.execute("SELECT name FROM workman")
        for i in self.cur.fetchall():
            self.workman1.append(i)
            self.listBox1.Append(i)
        self.c.close()
    def Izdeliya(self):
        self.c = db.connect(database=app.namepol)
        self.cur = self.c.cursor()
        self.cur.execute("SELECT name FROM Izdeliya")
        for i in self.cur.fetchall():
            self.izd.append(i)
            self.listBox2.Append(i)
        self.c.close()




class IzdeliyaFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(700, 700))
        self.panel = wx.Panel(self, size=(3000, 3000), pos=(0, 560))
        self.panel1 = wx.Panel(self, size=(3000, 561), pos=(680, 0))
        self.grid = wx.grid.Grid(self, size=(680, 560))
        self.grid.CreateGrid(1, 2)
        self.grid.EnableEditing(False)
        self.button1 = wx.Button(self.panel, id=-1, label="Добавить", pos=(20, 5), size=(70, 30), style=0)
        self.button2 = wx.Button(self.panel, id=-1, label="Удалить", pos=(100, 5), size=(70, 30), style=0)
        self.button3 = wx.Button(self.panel, id=-1, label="Изменить", pos=(180, 5), size=(70, 30), style=0)
        self.button4 = wx.Button(self.panel, id=-1, label="Вернуться", pos=(260, 5), size=(70, 30), style=0)
        self.Bind(wx.EVT_BUTTON, self.Izd, self.button1)
        self.Podg()
        self.Bind(wx.EVT_BUTTON, self.delite, self.button2)
        self.Bind(wx.EVT_BUTTON, self.Izm, self.button3)
        self.Bind(wx.EVT_BUTTON, self.Back, self.button4)

    def Back(self,event):
        app.frameIzd.Close()
        app.frameGrid.Show()
        app.SetTopWindow(app.frameGrid)
    def Izm(self,event):
        dlg = wx.TextEntryDialog(None, "Введите название изделия", "Изменение изделия", "Первое изделие")
        if dlg.ShowModal() == wx.ID_OK:
            self.response = dlg.GetValue()
        name = self.response
        dlg = wx.TextEntryDialog(None, "Введите цену изделия", "Изменение изделия", "100.0")
        if (dlg.ShowModal() == wx.ID_OK) and is_number(dlg.GetValue()):
            self.response = dlg.GetValue()
        else:
            dlg = wx.MessageDialog(None, 'Введите число', 'Ошибка!', wx.OK | wx.ICON_ERROR)
            if (dlg.ShowModal() == wx.ID_OK):
                dlg.Destroy()
            return
        value = self.response
        self.c = db.connect(database=app.namepol)  # Добавить проверку на совпадения с прошлыми рабочими
        self.cur = self.c.cursor()
        self.cur.execute("UPDATE Izdeliya SET value = '%s' WHERE name ='%s';"%(value, name))
        self.c.commit()
        self.Podg()
        self.grid.AutoSize()

    def delite(self,event):
        self.c = db.connect(database=app.namepol)
        self.cur = self.c.cursor()
        cells=self.grid.GetGridCursorRow()
        strr=self.grid.GetCellValue(cells,0)
        self.cur.execute("DELETE FROM Izdeliya WHERE name ='%s'"%strr)
        self.c.commit()
        self.Podg()


    def Podg(self):
        self.grid.ClearGrid()
        self.grid.SetColLabelValue(0, "Название")
        self.grid.SetColLabelValue(1, "Цена")

        self.c = db.connect(database=app.namepol)  # Добавить проверку на совпадения с прошлыми рабочими
        self.cur = self.c.cursor()
        self.cur.execute("SELECT name,value FROM Izdeliya")
        z = 0
        for i,y in self.cur.fetchall():
            if (self.grid.NumberRows-1)<z:
                self.grid.AppendRows(numRows=1)
            self.grid.SetCellValue(z, 0,"%s" %i)
            self.grid.SetCellValue(z, 1, "%s" % y)
            z=z+1
        self.c.close()
        self.grid.AutoSize()

    def Izd(self,event):
        dlg = wx.TextEntryDialog(None, "Введите название изделия", "Добавление нового изделия", "Первое изделие")
        if dlg.ShowModal() == wx.ID_OK:
            self.response = dlg.GetValue()
        name = self.response
        dlg = wx.TextEntryDialog(None, "Введите цену изделия", "Добавление нового изделия", "100.0")
        if (dlg.ShowModal() == wx.ID_OK) and is_number(dlg.GetValue()):
            self.response = dlg.GetValue()
        else:
            dlg = wx.MessageDialog(None, 'Введите число','Ошибка!', wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
            return
        value = self.response
        self.c = db.connect(database=app.namepol)  # Добавить проверку на совпадения с прошлыми рабочими
        self.cur = self.c.cursor()
        self.cur.execute("INSERT INTO Izdeliya VALUES ('%s','%s')" % (name, value))
        self.c.commit()
        self.Podg()




class GridFrame(wx.Frame):
    def __init__(self, parent, id, title):
        self.c = db.connect(database=app.namepol)
        self.cur = self.c.cursor()
        self.cur.execute("""
                    create table if not exists  DataBase (
                    Date TEXT,
                    name TEXT,
                    i0 INTEGER,
                    i1 INTEGER,
                    i2 INTEGER,
                    i3 INTEGER,
                    i4 INTEGER,
                    i5 INTEGER,
                    i6 INTEGER,
                    i7 INTEGER,
                    i8 INTEGER,
                    i9 INTEGER
                     );
                     """)
        c1.commit()
        wx.Frame.__init__(self, parent, id, title, size=(700, 700))
        self.panel = wx.Panel(self,size=(3000, 3000),pos=(0,560))
        self.grid = wx.grid.Grid(self, size=(680, 560))
        self.grid.CreateGrid(50, 11)
        self.grid. EnableEditing(False)
        self.button1 = wx.Button(self.panel, id=-1, label="Управление рабочими", pos=(3, 5), size=(150, 30), style=0)
        self.button2 = wx.Button(self.panel, id=-1, label="Управление изделиями", pos=(158, 5), size=(150, 30), style=0)
        self.button3 = wx.Button(self.panel, id=-1, label="Добавить", pos=(310, 5), size=(100, 30), style=0)
        self.button4 = wx.Button(self.panel, id=-1, label="Изменить", pos=(410, 5), size=(100, 30), style=0)
        self.button5 = wx.Button(self.panel, id=-1, label="Удалить", pos=(510, 5), size=(100, 30), style=0)
        self.Bind(wx.EVT_BUTTON, self.Work, self.button1)
        self.Bind(wx.EVT_BUTTON, self.Izdeliya, self.button2)
        self.Bind(wx.EVT_BUTTON, self.Add, self.button3)

    def Add(self,event):
        app.AddFrame()

    def Work(self,event):
        app.CreateWorkingFrame()

    def Izdeliya(self,event):
        app.IzdFrame()



class Workingframe(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(700, 700))
        self.panel = wx.Panel(self)
        self.listBox = wx.ListBox(self.panel, -1, (20, 20), (600, 600),[], wx.LB_SINGLE)
        self.button1 = wx.Button(self.panel, id=-1, label="Добавить", pos=(20, 625), size=(70, 30),style=0)
        self.button2 = wx.Button(self.panel, id=-1, label="Удалить", pos=(100, 625), size=(70, 30),style=0)
        self.button3 = wx.Button(self.panel, id=-1, label="Просмотр профиля рабочего", pos=(180, 625), size=(200, 30), style=0)
        self.Bind(wx.EVT_BUTTON, self.Workman, self.button1)
        self.Bind(wx.EVT_BUTTON, self.delite, self.button2)
        self.button4 = wx.Button(self.panel, id=-1, label="Вернуться", pos=(385, 625), size=(70, 30), style=0)
        self.Bind(wx.EVT_BUTTON, self.Back, self.button4)
        self.c = db.connect(database=app.namepol)
        self.cur = self.c.cursor()
        self.cur.execute("SELECT name FROM workman")
        self.listBox.Clear()
        for i in self.cur.fetchall():
            self.listBox.Append(i)
        self.c.close()


    def Back(self,event):
        app.frameworking.Close()
        app.frameGrid.Show()
        app.SetTopWindow(app.frameGrid)

    def delite(self,event):
        self.c = db.connect(database=app.namepol)  # Добавить проверку на совпадения с прошлыми рабочими
        self.cur = self.c.cursor()
        self.cur.execute("DELETE FROM workman WHERE name ='%s'"%self.listBox.GetString(self.listBox.GetSelection()))
        self.c.commit()
        self.cur.execute("SELECT name FROM workman")
        self.listBox.Clear()
        for i in self.cur.fetchall():
            self.listBox.Append(i)
        self.c.commit()
        self.c.close()
        self.cur.close()

    def Workman(self,event):
        dlg = wx.TextEntryDialog(None, "Введите имя рабочего", "Добавление нового рабочего", "Первый рабочий")
        if dlg.ShowModal() == wx.ID_OK:
            self.response = dlg.GetValue()
        name=self.response
        dlg = wx.TextEntryDialog(None, "Введите описание рабочего", "Добавление нового рабочего", "Описание")
        if dlg.ShowModal() == wx.ID_OK:
            self.response = dlg.GetValue()
        opisanie=self.response
        self.c = db.connect(database=app.namepol)  # Добавить проверку на совпадения с прошлыми рабочими
        self.cur = self.c.cursor()
        self.cur.execute("INSERT INTO workman(name,opisanie) VALUES ('%s','%s')"%(name,opisanie))
        self.c.commit()
        self.cur.execute("SELECT name FROM workman")
        self.listBox.Clear()
        for i in self.cur.fetchall():
            self.listBox.Append(i)
        self.c.close()



class App(wx.App):
    def __init__(self):  # Метод вызывающий начальный метод родительского класса
        wx.App.__init__(self)
    def OnInit(self):#Метод который автоматически запускается при создании класса
        #Создание  объекта класса окна
        self.frame = StartFrame(parent=None, id=-1, title='Практика Work')
        self.frame.Show()
        # Установить его главным
        self.SetTopWindow(self.frame)
        self.namepol = ""
        return True
    def CreateFrameGrid(self):
        self.frameGrid=GridFrame(parent=None, id=-1, title='Практика Work')
        self.frame.Close()
        self.frameGrid.Show()
        self.SetTopWindow(self.frameGrid)
    def CreateWorkingFrame(self):
        self.frameworking=Workingframe(parent=None, id=-1, title='Управление рабочими')
        self.frameGrid.Hide()
        self.frameworking.Show()
        self.SetTopWindow(self.frameworking)
    def IzdFrame(self):
        self.frameIzd = IzdeliyaFrame(parent=None, id=-1, title='Управление изделиями')
        self.frameGrid.Hide()
        self.frameIzd.Show()
        self.SetTopWindow(self.frameIzd)
    def AddFrame(self):
        self.frameAdd = AddFrame(parent=None, id=-1, title='Добавление сделанной работы')
        self.frameGrid.Hide()
        self.frameAdd.Show()
        self.SetTopWindow(self.frameAdd)



if __name__ == '__main__':
    c1 = db.connect(database="Profili")  # Добавить проверку на совпадения с прошлыми пользователями
    cur1 =c1.cursor()
    cur1.execute("""
            create table if not exists  Profili (
            name TEXT,
            countizd INTEGER DEFAULT 0
             );
             """)
    c1.commit()
    app = App()
    app.MainLoop()
