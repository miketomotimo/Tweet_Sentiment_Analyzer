import wx
import wx.grid as gridlib
import matplotlib.dates as mdates
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pubsub import pub
import numpy as np


class Panel1(wx.Panel):
    def __init__(self, parent):
        # constructor
        super(Panel1, self).__init__(parent=parent)
        self.parent = parent
        # font for the program title
        font = wx.Font(35, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # widgets
        title = wx.StaticText(self, wx.ID_ANY, label="Tweet_Sentiment_Analyzer_")
        title.SetFont(font)
        self.msg_text = wx.TextCtrl(self, wx.ID_ANY, value="")
        button = wx.Button(self, wx.ID_ANY, "Sentiment Analyze!")
        button.Bind(wx.EVT_BUTTON, self.parent.OnSwap, button)

        # sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title)
        sizer.Add(self.msg_text)
        sizer.Add(button)
        self.SetSizer(sizer, wx.ALIGN_CENTRE_HORIZONTAL)


class Panel2(wx.Panel):
    def __init__(self, parent):
        # constructor
        super(Panel2, self).__init__(parent=parent)
        self.parent = parent

        # widgets
        button = wx.Button(self, wx.ID_ANY, "Return to Main Menu")
        button.Bind(wx.EVT_BUTTON, self.parent.OnSwap, button)

        # graph creation
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self, -1, self.figure)

        # grid creation
        self.grid = gridlib.Grid(self)
        self.grid.CreateGrid(1,1)

        # sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(button)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(self.sizer)


class MainFrame(wx.Frame):
    def __init__(self, parent, df):
        # constructor
        super(MainFrame, self).__init__(parent=parent, title="Tweet Sentiment Analyzer")
        self.df = df
        # subscribe to topic
        pub.subscribe(self.KeywordFilter, "infotransfer")

        # make panels attributes of parent class
        self.panel_one = Panel1(self)
        self.panel_two = Panel2(self)
        self.panel_two.Hide()  # to make only panel 1 show initially

        # change panel background colour
        self.panel_one.SetBackgroundColour("#C7C6C1")
        self.panel_two.SetBackgroundColour("#C7C6C1")

        # add panels to sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def OnSwap(self, event):
        if self.panel_one.IsShown():
            # send message
            content = self.panel_one.msg_text.GetValue()
            pub.sendMessage("infotransfer", keyword=content)

            # swap panels
            self.SetTitle("Panel Two Showing")
            self.panel_one.Hide()
            self.panel_two.Show()
        else:
            # destroy and recreate grid
            # self.panel_two.grid.Destroy()
            # self.panel_two.grid = gridlib.Grid(self.panel_two)
            # self.panel_two.sizer.Add(self.panel_two.grid, 1, wx.EXPAND)
            # swap panels
            self.SetTitle("Panel One Showing")
            self.panel_two.Hide()
            self.panel_one.Show()
        self.Layout()

    def KeywordFilter(self, keyword, arg2=None):
        # listener function takes the dataframe and filters it, creating a new dataframe
        self.filtered_df = self.df

        if keyword:
            self.filtered_df = self.filtered_df[self.df["Tweet"].str.contains(keyword, case=False)]

        # update graph after df filtering
        dates = self.filtered_df.index
        values = self.filtered_df["Score"]
        x_dates = mdates.date2num(dates)  # convert data to mpl date format

        self.panel_two.ax.clear() # removes any previously plotted data
        self.panel_two.ax.plot_date(x_dates, values, color='black', label='Sentiment Over Time') # plot datetime using plot_date
        self.panel_two.ax.set_ylabel("Compound Score")  # set y label
        self.panel_two.ax.set_xlabel("Dates")  # set x label
        self.panel_two.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # change format on xaxis
        self.panel_two.canvas.draw()

        # remake grid after df filtering
        # gets shape of dataframe
        row_length = self.filtered_df.shape[0]
        column_length = self.filtered_df.shape[1]
        self.panel_two.grid.ClearGrid()  # clears grid
        self.panel_two.grid.DeleteCols(numCols=self.panel_two.grid.GetNumberCols())
        self.panel_two.grid.DeleteRows(numRows=self.panel_two.grid.GetNumberRows())
        self.panel_two.grid.AppendCols(numCols=column_length) # add columns
        self.panel_two.grid.AppendRows(numRows=row_length) # add rows

        column_names = self.filtered_df.columns.tolist()  # gets name of df columns

        # change size of columns
        self.panel_two.grid.SetColSize(0, 200)  # change size of Username column
        self.panel_two.grid.SetColSize(1, 700)  # change size of Tweet column

        # makes table columns names same as df columns
        for col in range(column_length):
            self.panel_two.grid.SetColLabelValue(col, column_names[col])

        # copy cells of df to grid
        for row in range(row_length):
            for col in range(column_length):
                self.panel_two.grid.SetCellValue(row, col, str(self.filtered_df.iloc[row, col]))


