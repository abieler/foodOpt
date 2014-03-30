#!/usr/bin/python2.7
from __future__ import division
import sys
import sqlite3
import os, sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


from PySide import QtCore as QTC
from PySide import QtGui as QTG

from pyswarm_2 import apsa
import ui_foodOptimizer
        
#class Window(QTG.QWidget,ui_foodOptimizer.Ui_Form):
class Window(QTG.QMainWindow, ui_foodOptimizer.Ui_MainWindow):
    message1 = QTC.Signal(int)


    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        
        self.resolution = QTG.QDesktopWidget().screenGeometry()
        
        self.language = 'D'
        self.connect(self.pushButton_search, QTC.SIGNAL("clicked()"), self.search)
        self.connect(self.pushButton_startOptimization, QTC.SIGNAL("clicked()"), self.startOptimization)
        self.connect(self.tableWidget_overview,QTC.SIGNAL("cellClicked(int, int)"), self.addItemClicked)
        self.connect(self.tableWidget_userSelection,QTC.SIGNAL("cellClicked(int, int)"), self.removeItemClicked)
        self.connect(self.tableWidget_userSelection,QTC.SIGNAL("cellChanged(int, int)"), self.modifyCellClicked)
        #self.connect(self.tableWidget_userSelection,QTC.SIGNAL("cellActivated(int, int)"), self.modifyCellClicked)
        self.connect(self.lineEdit_search,QTC.SIGNAL("textChanged(const QString&)"), self.search)
        
        self.message1.connect(self.updateProgressBar, QTC.Qt.QueuedConnection)
        self.add_menu_options()
        
        
        self.connect(self.tableWidget_overview.horizontalHeader(),QTC.SIGNAL("sectionResized(int, int, int)"),
                    self.tableWidget_overview, QTC.SLOT("resizeRowsToContents()"))
        
        self.x0 = False
        self.optimizer_thread = Optimizer()
        self.optimizer_thread.message.connect(self.plotOptimizedResult, QTC.Qt.QueuedConnection)
        self.set_language_env()
        
        #######################################################
        # create overview table
        ########################################################
        
        self.db, self.cur = self.setupDB()
        self.cur.execute("SELECT NAME_%s FROM naerwerte ORDER BY NAME_%s" % (self.language, self.language))
        data = self.cur.fetchall()
        self.setupView(data,1)
        
        
        #######################################################
        # create user selection table
        ########################################################
        self.tableWidget_userSelection.setColumnCount(5)
        self.tableWidget_userSelection.setHorizontalHeaderLabels([ 'Name', 'min [g]', 'max [g]', 'optimal','remove'])
        self.tableWidget_userSelection.setColumnWidth(0, self.resolution.width()/3)
            
            
        ###############################################################
        # set categories in combo box
        ###############################################################
        self.cur.execute("SELECT CATEGORY_%s FROM naerwerte" % self.language)
        data = self.cur.fetchall()
        catList = []
        for d in data:
            category = d[0].split('/')[0]
            if category not in catList:
                catList.append(category)
                
        catList.sort()
        for thing in catList:
            self.comboBox_categories.addItem(thing)
            
            
        self.getIdealValues()
        self.updateViewGraph()
        
    def add_menu_options(self):
        
        self.menuFile.addAction('save data',self.save_clicked)
        self.menuFile.addAction('load data', self.load_clicked)
        self.menuFile.addAction('settings...', self.settings_clicked)
        
        
    def settings_clicked(self):
        print 'preferences clicked'


    def save_clicked(self):
        print 'save clicked'
        saveName = QTG.QInputDialog.getText(self, 'save', self.tr("save as:"))
        print saveName[0]
        
        nrOfRows = self.tableWidget_userSelection.rowCount()
        for i in range(nrOfRows):
            foodItem = self.tableWidget_userSelection.item(i,0).text()
            userMin = np.float(self.tableWidget_userSelection.item(i,1).text())
            userMax = np.float(self.tableWidget_userSelection.item(i,2).text())
            try:
                userOpt = np.float(self.tableWidget_userSelection.item(i,3).text())
            except:
                userOpt = 0.0
            self.cur.execute('INSERT INTO saved_menus VALUES("%s", "%s", %f, %f, %f)' %(str(saveName[0]), foodItem, userMin, userMax, userOpt))
            
        self.db.commit()
        
        
    def load_clicked(self):
        
        self.cur.execute("SELECT savedName FROM saved_menus GROUP BY savedName")
        data = self.cur.fetchall()
        
        items = [item[0] for item in data]
        
        for d in data:
            print d
        
        loadName = QTG.QInputDialog.getItem(self, 'load', "load:", items, editable=False)[0]
        print loadName
        self.tableWidget_userSelection.setRowCount(0)
        self.cur.execute('SELECT * FROM saved_menus WHERE savedName = "%s"' %loadName)
        data = self.cur.fetchall()
        for row in data:
            print row
            self.addItemClicked(0,0,True,row[1], str(row[2]), str(row[3]), str(row[4]))

    def setupDB(self):
        db = sqlite3.connect('SwissFoodCompDataV50.sqlite')
        cur = db.cursor()
        
        return db,cur


    def set_language_env(self):
            if self.language == 'D':
                self.pltTitle = '% des Bedarfs'
                self.pltXticks = ['kcal', 'Fett', 'Protein', 'Na', 'vitA', 'vitB12', 'Zucker']
            elif self.language == 'E':
                self.pltTitle = '% of needed amount'
                self.pltXticks = ['kcal','fat','protein','sodium','vitA','vitB12', 'sugar']


    def getIdealValues(self):
        
        if self.radioButton_singleMeal.isChecked():
            N = 1/3.0
        elif self.radioButton_oneDay.isChecked():
            N = 1
        elif self.radioButton_sevenDays.isChecked():
            N = 7
            
        
        self.kcalIdeal = 2000 * N
        self.proteinIdeal = 59 * N
        self.fatIdeal = 60 * N
        self.vitAIdeal = 1 * N
        self.B12Ideal = 3.0 * N
        self.sodiumIdeal = 2000 * N
        self.sugarIdeal = 55 * N
            
    def updateViewGraph(self):
        self.getIdealValues()
        try:
            finalResultMin = np.array([
                            self.energy_kcaMin/ self.kcalIdeal,
                            self.fatMin / self.fatIdeal,
                            self.proteinMin / self.proteinIdeal,
                            self.sodiumMin / self.sodiumIdeal,
                            self.vit_aMin / self.vitAIdeal,
                            self.b12Min / self.B12Ideal,
                            self.sugarMin / self.sugarIdeal
                        ]) * 100
            
            finalResultMax = np.array([
                            self.energy_kcaMax/ self.kcalIdeal,
                            self.fatMax / self.fatIdeal,
                            self.proteinMax / self.proteinIdeal,
                            self.sodiumMax / self.sodiumIdeal,
                            self.vit_aMax / self.vitAIdeal,
                            self.b12Max / self.B12Ideal,
                            self.sugarMax / self.sugarIdeal
                        ]) * 100
            
            finalResultOpt = np.array([
                            self.energy_kcaOpt/ self.kcalIdeal,
                            self.fatOpt / self.fatIdeal,
                            self.proteinOpt / self.proteinIdeal,
                            self.sodiumOpt / self.sodiumIdeal,
                            self.vit_aOpt / self.vitAIdeal,
                            self.b12Opt / self.B12Ideal,
                            self.sugarOpt / self.sugarIdeal
                        ]) * 100
        except Exception, e:
            pass
            #print 'Error plotting 1:'
            #print e
        try:
            indices = np.arange(7)
        except:
            pass
        width1 = 0.5
        width2 = 0.35
        
        self.mpl_widget.ax.clear()
        
        self.mpl_widget.ax.plot(np.arange(-1,len(indices)+1), np.ones(len(indices)+2)*100,'--k', linewidth=2)
        self.mpl_widget.ax.plot(np.arange(-1,len(indices)+1), np.zeros(len(indices)+2),'-k')
        
        try:
            self.mpl_widget.ax.bar(indices-width1/2, finalResultMax, width1, facecolor='#32A0DE')
        except Exception, e:
            pass
            #print 'Error plotting 2:'
            #print e
            
        try:
            self.mpl_widget.ax.bar(indices-width2/2, finalResultMin, width2, facecolor='#1C2F39')
        except Exception, e:
            pass
            #print 'Error plotting 3'
            #print e
        try:
            self.mpl_widget.ax.plot(indices,finalResultOpt,'or', markersize=12)
        except Exception,e:
            pass
            #print 'Error plotting 4'
            #print e
        self.mpl_widget.ax.grid(True)
        try:
            self.mpl_widget.ax.set_xticks(indices)
        except:
            pass
        try:
            #self.mpl_widget.ax.set_xticklabels(['kcal','fat','protein','sodium','vitA','vitB12', 'sugar'])
            self.mpl_widget.ax.set_xticklabels(self.pltXticks)
        except:
            pass
            
        self.mpl_widget.ax.set_title(self.pltTitle)
        self.mpl_widget.draw()


    def plotOptimizedResult(self,msg):

        x = self.xopt
        self.fatOpt, self.proteinOpt, self.energy_kcaOpt,self.charbohydrOpt,self.charbohydr2Opt,self.sugarOpt,self.sodiumOpt,self.vit_aOpt,self.b1Opt,self.b2Opt,self.b6Opt,self.b12Opt = 0,0,0,0,0,0,0,0,0,0,0,0
        nrOfRows = self.tableWidget_userSelection.rowCount()
        for k in range(nrOfRows):
            itemName = self.tableWidget_userSelection.item(k,0).text()
            fat_i, protein_i, energy_kca_i,charbohydr_i,charbohydr2_i,sugar_i,sodium_i,vit_a_i,b1_i,b2_i,b6_i,b12_i = self.getFoodInformation(itemName,self.cur)
            
            optAmount = x[k]
            foodItem = QTG.QTableWidgetItem()
            foodItem.setFlags(QTC.Qt.ItemIsEnabled)
            foodItem.setText(str(optAmount))
            self.tableWidget_userSelection.setItem(k,3, foodItem )
            
            self.fatOpt += fat_i * optAmount / 100
            self.proteinOpt += protein_i* optAmount / 100
            self.energy_kcaOpt += energy_kca_i* optAmount / 100
            self.charbohydrOpt += charbohydr_i* optAmount / 100
            self.charbohydr2Opt += charbohydr2_i* optAmount / 100
            self.sugarOpt += sugar_i* optAmount / 100
            self.sodiumOpt += sodium_i* optAmount / 100
            self.vit_aOpt += vit_a_i* optAmount / 10**5
            self.b1Opt += b1_i* optAmount / 100
            self.b2Opt += b2_i* optAmount / 100
            self.b6Opt += b6_i* optAmount / 100
            self.b12Opt += b12_i* optAmount / 100
            
        self.modifyCellClicked(0,2)

    def modifyCellClicked(self,i,j):
        
        if j == 2 and (len(self.tableWidget_userSelection.item(i,j).text()) > 0):
            self.fatMin, self.proteinMin, self.energy_kcaMin,self.charbohydrMin,self.charbohydr2Min,self.sugarMin,self.sodiumMin,self.vit_aMin,self.b1Min,self.b2Min,self.b6Min,self.b12Min = 0,0,0,0,0,0,0,0,0,0,0,0
            self.fatMax, self.proteinMax, self.energy_kcaMax,self.charbohydrMax,self.charbohydr2Max,self.sugarMax,self.sodiumMax,self.vit_aMax,self.b1Max,self.b2Max,self.b6Max,self.b12Max = 0,0,0,0,0,0,0,0,0,0,0,0
            nrOfRows = self.tableWidget_userSelection.rowCount()
            for k in range(nrOfRows):
                itemName = self.tableWidget_userSelection.item(k,0).text()
                fat_i, protein_i, energy_kca_i,charbohydr_i,charbohydr2_i,sugar_i,sodium_i,vit_a_i,b1_i,b2_i,b6_i,b12_i = self.getFoodInformation(itemName,self.cur)
                try:
                    minAmount = self.tableWidget_userSelection.item(k,1).text()
                    minAmount = np.float(minAmount)
                except:
                    minAmount = 0
                try:
                    maxAmount = self.tableWidget_userSelection.item(k,2).text()
                    maxAmount = np.float(maxAmount)
                except:
                    maxAmount = 0
     
                try:
                    self.fatMin += fat_i * minAmount / 100
                    self.proteinMin += protein_i* minAmount / 100
                    self.energy_kcaMin += energy_kca_i* minAmount / 100
                    self.charbohydrMin += charbohydr_i* minAmount / 100
                    self.charbohydr2Min += charbohydr2_i* minAmount / 100
                    self.sugarMin += sugar_i* minAmount / 100
                    self.sodiumMin += sodium_i* minAmount / 100
                    self.vit_aMin += vit_a_i* minAmount / 10**5
                    self.b1Min += b1_i* minAmount / 100
                    self.b2Min += b2_i* minAmount / 100
                    self.b6Min += b6_i* minAmount / 100
                    self.b12Min += b12_i* minAmount / 100
                except Exception, e:
                    print 'Error modifyCellClicked 1'
                    print e
                try:
                    self.fatMax += fat_i * maxAmount / 100
                    self.proteinMax += protein_i* maxAmount / 100
                    self.energy_kcaMax += energy_kca_i* maxAmount / 100
                    self.charbohydrMax += charbohydr_i* maxAmount / 100
                    self.charbohydr2Max += charbohydr2_i* maxAmount / 100
                    self.sugarMax += sugar_i* maxAmount / 100
                    self.sodiumMax += sodium_i* maxAmount / 100
                    self.vit_aMax += vit_a_i* maxAmount / 10**5
                    self.b1Max += b1_i* maxAmount / 100
                    self.b2Max += b2_i* maxAmount / 100
                    self.b6Max += b6_i* maxAmount / 100
                    self.b12Max += b12_i* maxAmount / 100
                except Exception, e:
                    print 'Error modifyCellClicked 2'
                    print e
                
            self.updateViewGraph()
            
    def getFoodInformation(self,itemName,cur):
        query = 'SELECT PROTEIN, FAT, ENERGY_KCA, CHARBOHYDR, CHARBOHYD2, SUGAR, SODIUM, VIT_A, B1, B2, B6, B12 FROM naerwerte WHERE NAME_%s LIKE "%%%s%%"' % (self.language, itemName)
        #print query
        cur.execute(query)
        data = cur.fetchall()
        PROTEIN, FAT, ENERGY_KCA, CHARBOHYDR, CHARBOHYD2, SUGAR, SODIUM, VIT_A, B1, B2, B6, B12 = data[0]
        
        return PROTEIN, FAT, ENERGY_KCA, CHARBOHYDR, CHARBOHYD2, SUGAR, SODIUM, VIT_A, B1, B2, B6, B12
        
        
    def removeItemClicked(self,i,j):
        
        if j == 4:
            print 'remove item'
            self.tableWidget_userSelection.removeRow(i)
            
        self.modifyCellClicked(0,0)
    
    def addItemClicked(self,i,j,loaded=False,foodItem=None, userMin=None, userMax=None, userOpt=None):
        
        if j == 0:
            if not loaded:
                text = self.tableWidget_overview.item(i,0).text()
            else:
                text = foodItem
            
            nrOfRows = self.tableWidget_userSelection.rowCount()
            self.tableWidget_userSelection.insertRow(nrOfRows)
            
            addedItem = QTG.QTableWidgetItem()
            addedItem.setFlags(QTC.Qt.ItemIsEnabled)
            addedItem.setText(text)
            self.tableWidget_userSelection.setItem(nrOfRows,0, addedItem)
            

            minItem = QTG.QTableWidgetItem()
            #minItem.setFlags(QTC.Qt.ItemIsEnabled)
            minItem.setText(userMin)
            self.tableWidget_userSelection.setItem(nrOfRows, 1, minItem)
        
            maxItem = QTG.QTableWidgetItem()
            #minItem.setFlags(QTC.Qt.ItemIsEnabled)
            maxItem.setText(userMax)
            self.tableWidget_userSelection.setItem(nrOfRows, 2, maxItem)
        
            optItem = QTG.QTableWidgetItem()
            optItem.setFlags(QTC.Qt.ItemIsEnabled)
            optItem.setText(userOpt)
            self.tableWidget_userSelection.setItem(nrOfRows, 3, optItem)
            
            removeItem = QTG.QTableWidgetItem()
            removeItem.setFlags(QTC.Qt.ItemIsEnabled)
            removeItem.setText('remove')
            self.tableWidget_userSelection.setItem(nrOfRows,4, removeItem )

    
    def setupView(self,data,init=0):
        
        self.tableWidget_overview.setColumnCount(1)
        self.tableWidget_overview.setHorizontalHeaderLabels([ 'Name'])
        self.tableWidget_overview.setRowCount(len(data))
        self.tableWidget_overview.setWordWrap(True)
        
        for d,i in zip(data,range(len(data))):
            foodItem = QTG.QTableWidgetItem()
            foodItem.setFlags(QTC.Qt.ItemIsEnabled)
            foodItem.setText(d[0].strip().replace('"',''))
            self.tableWidget_overview.setItem(i,0, foodItem )
            
        if init == 1:
            self.tableWidget_overview.resize(self.resolution.width()/3, self.resolution.width()/3)
            self.tableWidget_overview.setColumnWidth(0, self.resolution.width()/3)
            
            
    def search(self):
        if len(self.lineEdit_search.text()) >= 1:
            searchPattern = self.lineEdit_search.text()
            query = 'SELECT NAME_%s, ENERGY_KCA, PROTEIN, FAT FROM naerwerte WHERE NAME_%s LIKE "%%%s%%" ORDER BY NAME_%s' % (self.language, self.language, searchPattern, self.language)
            
        else:
            category = self.comboBox_categories.currentText()
            query =  'SELECT NAME_%s, ENERGY_KCA, PROTEIN, FAT FROM naerwerte WHERE CATEGORY_%s LIKE "%%%s%%" ORDER BY NAME_%s' %(self.language, self.language, category, self.language)
        
        self.cur.execute(query)
        data = self.cur.fetchall()
        self.setupView(data)
        
    def computeResults(self,x,additionalData):
        
        PROTEIN = np.sum(additionalData[:,0] * x / 100)
        FAT = np.sum(additionalData[:,1] * x / 100)
        ENERGY_KCA = np.sum(additionalData[:,2] * x / 100)
        CHARBOHYDR = np.sum(additionalData[:,3] * x)
        CHARBOHYD2 = np.sum(additionalData[:,4] * x)
        SUGAR = np.sum(additionalData[:,5] * x)
        SODIUM = np.sum(additionalData[:,6] * x / 100)
        VIT_A = np.sum(additionalData[:,7] * x / 10**5)
        B1 = np.sum(additionalData[:,8] * x)
        B2 = np.sum(additionalData[:,9] * x)
        B6 = np.sum(additionalData[:,10] * x)
        B12 = np.sum(additionalData[:,11] * x / 100)
        
        
        
        finalResult = np.array([
                                ENERGY_KCA/ self.kcalIdeal,
                                FAT / self.fatIdeal,
                                PROTEIN / self.proteinIdeal,
                                SODIUM / self.sodiumIdeal,
                                VIT_A / self.vitAIdeal,
                                B12 / self.B12Ideal,
                            ]) * 100 + 0.1
        
        indices = np.arange(len(finalResult))
        width = 0.35
        plt.figure()
        plt.bar(indices-width/2,finalResult,width,bottom=None, hold= None)
        plt.xticks(indices, ['kcal\n%i%%'% ((ENERGY_KCA/ self.kcalIdeal) * 100),
                             'fat\n%i%%'% ((FAT / self.fatIdeal)*100),
                             'protein\n%i%%'% ((PROTEIN / self.proteinIdeal)*100),
                             'sodium\n%i%%'% ((SODIUM / self.sodiumIdeal)*100),
                             'vitA\n%i%%'% ((VIT_A / self.vitAIdeal)*100),
                             'vitB12\n%i%%'% ((B12 / self.B12Ideal)*100)])
        plt.title('Nutrition overview % of daily need')
        plt.grid(True)
        plt.show()
        
    def updateProgressBar(self, finished):
        #print 'finished:', finished
        self.progress.setValue(int(finished))
        
        
    def func(self,x, iteration, particleNr,additionalData):
        
        
        if iteration % (self.optimizer_thread.maxIterations / 50) == 0:
            self.message1.emit(iteration / 1000 * 100)
        
        PROTEIN = np.sum(additionalData[:,0] * x / 100)
        FAT = np.sum(additionalData[:,1] * x / 100)
        ENERGY_KCA = np.sum(additionalData[:,2] * x / 100)
        CHARBOHYDR = np.sum(additionalData[:,3] * x)
        CHARBOHYD2 = np.sum(additionalData[:,4] * x)
        SUGAR = np.sum(additionalData[:,5] * x)
        SODIUM = np.sum(additionalData[:,6] * x / 100)
        VIT_A = np.sum(additionalData[:,7] * x / 10**5)
        B1 = np.sum(additionalData[:,8] * x)
        B2 = np.sum(additionalData[:,9] * x)
        B6 = np.sum(additionalData[:,10] * x)
        B12 = np.sum(additionalData[:,11] * x / 100)
        
        energy_score = (self.kcalIdeal - ENERGY_KCA)**2 + 1
        protein_score = (PROTEIN - self.proteinIdeal)**2 + 1
        fat_score = (self.fatIdeal- FAT)**2 + 1
        
        if (self.vitAIdeal < VIT_A):
            vitA_score = (self.vitAIdeal - VIT_A)**2 + 1
        else:
            vitA_score = abs(self.vitAIdeal - VIT_A) + 1
            
        if (self.B12Ideal < B12):
            vitB12_score = (self.B12Ideal - B12)**2 + 1
        else:
            vitB12_score = abs(self.B12Ideal - B12)**2 + 1
        
        if (self.sodiumIdeal > SODIUM):
            sodium_score = (self.sodiumIdeal - SODIUM)**2 + 1
        else:
            sodium_score = abs(self.sodiumIdeal - SODIUM)**2 + 1
        
        if (self.sugarIdeal > SUGAR):
            sugar_score = (self.sugarIdeal - SUGAR)**2 + 1
        else:
            sugar_score = abs(self.sugarIdeal - SUGAR)**2 + 1

        score = energy_score * protein_score * fat_score * vitA_score * vitB12_score * sodium_score * sugar_score
        
        return score


    def startOptimization(self):

        self.progress = QTG.QProgressDialog("Optimizing...", "OK", 0, 100, self)
        self.progress.setModal(True)
        self.progress.show()

        self.optimizer_thread.start()
 
 
class Optimizer(QTC.QThread):
    message = QTC.Signal(str)


    def __init__(self, parent = None):
        QTC.QThread.__init__(self,parent)
        self.signal = QTC.SIGNAL("signal")
 
 
    def run(self):

        db,cur = window.setupDB()

        if window.radioButton_singleMeal.isChecked():
            N = 1 / 3.0
        elif window.radioButton_oneDay.isChecked():
            N = 1
        elif window.radioButton_sevenMeals.isChecked():
            N = 7

        window.kcalIdeal = 2000 * N
        window.proteinIdeal = 59 * N
        window.fatIdeal = 60 * N
        window.vitAIdeal = 1 * N
        window.B12Ideal = 3.0 * N
        window.sodiumIdeal = 550 * N

        additionalData = []
        x0 = []
        xmin = []
        xmax = []
        nrOfItems = window.tableWidget_userSelection.rowCount()
        for i in range(nrOfItems):
            itemName =  window.tableWidget_userSelection.item(i,0).text()
            additionalData.append(window.getFoodInformation(itemName,cur))
            xmin.append(np.float(window.tableWidget_userSelection.item(i,1).text()))
            xmax.append(np.float(window.tableWidget_userSelection.item(i,2).text()))

        db.close()
        xmin = np.array(xmin)
        xmax = np.array(xmax)
        
        if window.x0 and (len(window.x0) == len(xmin)):
            x0 = window.x0
        else:
            x0 = xmin + (xmax - xmin)/2
        dx = (xmax - xmin)/2
            
        additionalData = np.array(additionalData)
        
        self.maxIterations = 1000
        
        fopt, xopt = apsa(window.func, x0,dx,xmin,xmax,20,self.maxIterations,additional_data = additionalData)
        print fopt, xopt

        window.x0 = xopt
        window.xopt = xopt
        self.message.emit("blaaaa")
        
        
app = QTG.QApplication(sys.argv)
window = Window()
window.showMaximized()
sys.exit(app.exec_())
