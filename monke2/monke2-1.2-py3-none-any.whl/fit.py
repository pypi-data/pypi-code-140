
# from re import I
# from click import style
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from matplotlib import container


class linear_fit():
    from matplotlib.offsetbox import AnchoredText

   # Style des Diagramms
    style = 'default'
    try:
        style = ['notebook','grid','science']
    except:
        try:
            style = ['default','grid']
        except:
            style='default'

    size = 16
    def _size(self):
        BIG = self.size 
        SMALL = self.size * 0.6
        MID = self.size * 0.75
        plt.rc('font', size=MID)          # controls default text sizes
        plt.rc('axes', titlesize=BIG)     # fontsize of the axes title
        plt.rc('axes', labelsize=MID)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL)    # legend fontsize
        plt.rc('figure', titlesize=BIG)  # fontsize of the figure title

    x_mittel = 0
    m_val = 1
    n_val = 1
    x_val = 1
    y_val = 1
    n_err = 0
    m_err = 0
    Vmn = 0


    # Ausfürhlichkeit der Infos die beim Fit ausgegeben werden
    detail = False

    #-----------------------------------------------------------------
    #least squares zur Angabe der Güte des Plots
    def __chi2(self):
        self.chi = (1/len(self.x_val)*((self.__f(self.x_val) - self.y_val)**2/np.asarray(self.y_err)**2).sum()).round(2)
        return self.chi


    #---WICHTIG!!!!!!!!!!!!---------------------------------------------------
    # Definiere Fehler des Scatter Plots ------------------------------------------
    # BEACHTE: falls der Fehler eine float-zahl ist, muss diese erst im [] geschrieben werden und mit der Anzahl der
    # Messwerte multiplizert werden, um eine Liste mit entsprechender Länge zu erstellen
    def set_y_error(self,yerr,var=True):
        # y_err muss ein Array sein. Wenn es nicht schon eins ist sondern ein skalar, dann erstelle ein array
        if type(yerr) == np.ndarray or type(yerr) == list:
            self.y_err = yerr
        elif type(yerr) == np.float64 or type(yerr) == float or type(yerr) == int:
            self.y_err = np.array([yerr])

        self.y_var = var

        return self.y_err

    def set_x_error(self,xerr):
        # x_err muss ein Array sein. Wenn es nicht schon eins ist sondern ein skalar, dann erstelle ein array
        if type(xerr) == np.ndarray or type(xerr) == list:
            self.x_err = xerr
        elif type(xerr) == np.float64 or type(xerr) == float or type(xerr) == int:
            self.x_err = np.array([xerr])


        return self.x_err


    #setze individuelles Runden für m und n
    m_round = ''
    n_round = ''

    # extra boolean, um die Ergebnissausgabe zu verhindern
    HIDE = False

    # Gebe die Ergebnisse Aus 
    def print_res(self, result,name , hide):
        if hide == False:
            print('----------------------------')
            if name != '':
                print(name)
            if self.detail == True:
                print('x:', result['x'])
                print('x^2:', result['xx'])
                print('y:', result['y'])
                print('sigma^2:' , result['Vy'])
            print('m:', result['m'],'+-',result['merr'])
            print('n:', result['n'],'+-',result['nerr'])
            print('goodness:', self.chi)     # soll minimum sein für guten Fit
            print('----------------------------')


    # Erstelle Eigene Profile mit individuellen Aussehen
    def profile(self,name):
        if name == 'Gabriel':
            self.legendsize = 9
            self.errbar = [7,5,1,1,'x']
            self.plotsize = (6,4)
            try:
                str_vals = [0]*4
                for i,j in enumerate([self.m_val,self.m_err,self.n_val,self.n_err]):
                    str_vals[i] = np.array([j])
                str_vals[0], str_vals[1] = error_round(str_vals[0], str_vals[1])
                str_vals[2], str_vals[3] = error_round(str_vals[2], str_vals[3])
                self.legend_label[0] = '$f(x) =($'+str_vals[0][0]+'$\\pm$'+str_vals[1][0]+'$)x + ($'+str_vals[2][0]+'$\\pm$'+str_vals[3][0]+')'
            except:
                print('error: konnte legend_label nicht setzen')
            
        elif name == 'Christian':
            self.errbar = [7,5,1.5,1.5,'x']
            self.plotsize = (10,6)
            self.ANCH = 25
            self.size = 25
            self.legendsize = 15
            self.colors[1] = 'cornflowerblue'
            try:
                #self.legend_label[0] = '$f(x) =($'+str(self.m_val)+'$\\pm$'+str(self.m_err)+'$)x + ($'+str(self.n_val)+'$\\pm$'+str(self.n_err)+')'
                str_vals = [0]*4
                for i,j in enumerate([self.m_val,self.m_err,self.n_val,self.n_err]):
                    str_vals[i] = np.array([j])
                str_vals[0], str_vals[1] = error_round(str_vals[0], str_vals[1])
                str_vals[2], str_vals[3] = error_round(str_vals[2], str_vals[3])
                self.legend_label[0] = '$f(x) =($'+str_vals[0][0]+'$\\pm$'+str_vals[1][0]+'$)x + ($'+str_vals[2][0]+'$\\pm$'+str_vals[3][0]+')'
            except:
                print('error: konnte legend_label nicht setzen')
        else:
            print('profile not found')


    #---WICHTIG!!!!!!!!!!!!--------------------------------------------------- 
    # hiermit werden alle Daten nach belieben varianzgewichtet ausgewertet
    def make_fit(self,x_vals,y_vals,r=2,str='', hide=''):

        if hide != '':                                # kontrolliert, welchen Wert HIDE hat
            self.HIDE = hide
        
        if self.m_round == '':                        #setze m,n nachkommastellen
            self.m_round = r   

        if self.n_round == '':                        #setze m,n nachkommastellen
            self.n_round = r 
    

        #-setze die globalen variablen auf die Werte der make_fit function
        self.x_val=x_vals      
        self.y_val=y_vals

        #-breche Funktion ab, wenn y-fehler nicht definiert wurde, da dieser wichtig zur weiteren Berechnung ist 
        # (für die varianzgewichtete Standardabweichung)
        if self.y_err[0]==0:
            print('Acthung: bitte y-Fehler setzen')
            return 0

        # berechne mittelwerte (Varianzgewichtet) 
        # err ist dummy array für den error, falls der error nur eine float ist und kein array 
        # Dies ist wichtig zur einfachen Berechnung
        if self.y_var == True:
            if self.HIDE == False:
                print('VARIANZGEWICHTET')
            if len(self.y_err) == 1:
                err = np.zeros(len(x_vals))
                err[:] = float(self.y_err[0])
            else:
                err = self.y_err
            err = np.asarray(err)
            y = round(mittel_varianzgewichtet(y_vals,err),r)
            x = round(mittel_varianzgewichtet(x_vals,err),r)
            xx = round(mittel_varianzgewichtet(x_vals**2,err),r)
        else:
        # nicht varianzgewichtet sind die Mittelwerte einfache arithmetische Mittel
            if self.HIDE == False:
                print('NICHT VARIANZGEWICHTET')
            y = round(np.mean(y_vals),r)
            x = round(np.mean(x_vals),r)
            xx = round(np.mean(x_vals**2),r)

        # zur Berechnung der Varianzen Vxy und Vx benötigen wir die Mittelwerte als arrays
        x_arr = np.zeros(len(x_vals))
        x_arr[:] = x
        y_arr = np.zeros(len(y_vals))
        y_arr[:] = y 
        
        # Berechne Varianzen
        Vxy = varianz_xy(x_vals,x_arr,y_vals,y_arr)
        Vx = varianz_x(x_vals,x_arr)

        # Berechne y-Varianz. Unterscheide, ob es einen einheitlichen y-Fehler gibt oder jeder Messwert einen individuellen hat
        if len(self.y_err) == 1:
            Vy = len(x_vals) / (1/np.asarray(([self.y_err]*len(x_vals)))**2).sum()
        else:
            # Varianzgewichtete Varianz, da mit standardvarianz es nicht funktioniert
            Vy = len(x_vals) / (1/self.y_err**2).sum()    
        Vm = Vy/(len(x_vals)*(xx-x**2))
        Vn = xx * Vm
        Vmn = - Vm * x
        #sigma = np.sqrt(Vy)

        # Berechne die Steigung m und den Achsenabschnitt n der Geraden
        m = round(Vxy/Vx,self.m_round)
        n = round(y-m*x,self.n_round)

        # Berechne Fehler der Steigung m und des Achsenabschnitts n der Geraden
        merr = roundup(np.sqrt(Vm),self.m_round)
        nerr = roundup(np.sqrt(Vn),self.n_round)

        # Verwandle floats ohne Nachkommastellen in integer
        if self.m_round == 0:
            m, merr = int(m), int(merr)
        if self.n_round == 0:
            n, nerr = int(n), int(nerr)

        # globale Variablen erhalten Werde der make_fit function
        self.m_err = merr
        self.n_err = nerr
        self.x_mittel = x
        self.n_val = n
        self.m_val = m
        self.Vmn = Vmn

        # Berechne die Güte mit der least_squares Methode
        self.__chi2()

        result = {
            'x' :x,
            'xx' :xx,
            'y' :y,
            'm' : m,
            'n' : n,
            'merr' : merr,
            'nerr' : nerr,
            'Vm' : round(Vm,r),
            'Vn' : round(Vn,r),
            'Vxy' : round(Vxy,r),
            'Vy' : round(Vy,2),
            'Vmn' : round(Vmn,r),
            'x_vals' : x_vals,
            'y_vals' : y_vals,
            'yerr' : self.y_err
        }

        self.print_res(result,name=str ,hide=self.HIDE)
        return result

    # private Geraden Funktion  der Form f(x):=mx+n
    def __f(self,x):
        return self.n_val + self.m_val*x
        

    y_var = False
    y_err = [0]
    x_err = [0]

    # Gebe y- und x-Fehler aus als Array falls noch kein Array
    def __get_error(self):
        if(len(self.y_err) == 0):
            self.y_err = [self.y_err]*len(self.x_val)
        if(len(self.x_err) == 0):
            self.x_err = [self.x_err]*len(self.x_val)
        if(self.y_err[0] == 0):
            self.y_err = [0]*len(self.x_val)
        if(self.x_err[0] == 0):
            self.x_err = [0]*len(self.x_val)
        return self.y_err,self.x_err


    # die textloc variable bestimmt die Stelle, an der sich die weiteren Infos im Graphen befinden
    textloc = 'upper right'


    #--Wichtig---------------------------
    # erstellt optionale Fehlerkurven
    def _s(self,val):
        return np.sqrt(self.m_err**2*val**2+self.n_err**2+2*self.Vmn*val)

    #OPTIONAL
    #ändere die Größe des ausgegebenen Plots
    plotsize = (6,4)

    #OPTIONAL
    #ändere das Aussehen der Errorbars
    errbar = [5,5,1,1,'o'] # marker, caps, eline, markerwidth
    ANCH = 7

    #größe der Legende
    legendsize = 11
    legend_label = ['Geraden-Fit','Messwerte']
   
    # die Variablen der Limits des Diagramms
    ylim = (0,0)
    xlim = (0,0)

    # Setze die Ticks der Achsen
    xticks = 0
    yticks = 0

    # Rotation der Achsenbeschriftung
    xrotation = 0
    yrotation = 0

    # ändere die Farben im Diagramm
    colors = ['tab:red', 'black', 'black', 'steelblue']
    dpi = 300

    #---WICHTIG!!!!!!!!!!!!---------------------------------------------------
    # hiermit kann ein optionaler Plot erstellt werden
    def plot(self,title='title',xlabel='x_Achse',ylabel='y_achse',err=True,legend=True, infos = False ,name='',hide=False):

        # Erstellt das Diagramm
        plt.style.use('default') # verhindert, dass Fehler bei der Anzeige entstehen
        plt.style.use(self.style)
        self._size()
        

        plt.rcParams['figure.dpi'] = 120
        fig, ax = plt.subplots(figsize=self.plotsize)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        # setze die limits der achsen
        if self.ylim != (0,0):
            ax.set_ylim(self.ylim)
        if self.xlim != (0,0):
            ax.set_xlim(self.xlim)
        
        #setze die ticks der achsen
        try:
            if self.xticks != 0:
                plt.xticks(self.xticks)
            if self.yticks != 0:
                plt.yticks(self.yticks)
        except:
            print('error: konnte nicht ticks setzen')
        
        ax.tick_params(axis='x', labelrotation=self.xrotation)
        ax.tick_params(axis='y', labelrotation=self.yrotation)
        
        # Erstelle Errorbar 
        self.__get_error()
        ax.errorbar(self.x_val, self.y_val,color=self.colors[0],marker=self.errbar[4],markersize=self.errbar[0],linestyle='',zorder=10,
        yerr=self.y_err, xerr=self.x_err,label=self.legend_label[1],capsize=self.errbar[1], elinewidth=self.errbar[2], markeredgewidth=self.errbar[3])
        
        #bekomme momentane xlim
        left, right = ax.get_xlim()
        x_axis = np.linspace(left,right,20)

        #ax.plot(self.x_val, self.__f(self.x_val),color=self.colors[1],label=self.legend_label[0])
        if hide == False:
            ax.plot(x_axis, self.__f(x_axis),color=self.colors[1],label=self.legend_label[0],zorder=0)

        if self.detail == True and self.HIDE == False:
            print('f(x[0]): +-', self.__f(self.x_val[0]).round(2))
            print('f(x_letztes): +-', self.__f(self.x_val[(len(self.x_val)-1)]).round(2))
            print('----------------------------')

        # Erstelle Fehlerkurven um die Geraden herum, falls err==True gesetzt wurde
        if(err==True and hide == False):
            ax.plot(x_axis, self.__f(x_axis)+self._s(x_axis),'--',color=self.colors[2],zorder=0,alpha=0.8,lw=1.3,label='Fehlerkurve')
            ax.plot(x_axis, self.__f(x_axis)-self._s(x_axis),'--',color=self.colors[2],zorder=0,alpha=0.8,lw=1.3)

            # Fülle den Raum zwischen beiden Fehlerkurven mit einer Farbe
            plt.gca().fill_between(x_axis, self.__f(x_axis)+self._s(x_axis), self.__f(x_axis)-self._s(x_axis),
             alpha=0.25,color=self.colors[3])


            # Gebe den Anfangs-, Mittleren- und Endwert der Fehlerkurve bei Bedarf aus, damit man besser abzeichnen kann
            if self.detail == True and self.HIDE == False:
                print('s(x[0]): +-', self._s(self.x_val[0]).round(2))
                print('s(x_mittel): +-', self._s(self.x_mittel).round(2)) 
                print('s(x_letztes): +-', self._s(self.x_val[(len(self.x_val)-1)]).round(2))

        # füge manuelle Plots hinzu:
        try:
            if self.custom_multi_array != 0:
                for i in range(np.shape(self.custom_plot_x)[1]):
                    ax.plot(self.custom_plot_x[:,i],self.custom_plot_y[:,i],label=self.custom_label[i],color = self.custom_colors[i],zorder=2)
            else:
                ax.plot(self.custom_plot_x,self.custom_plot_y,label=self.custom_label,color = self.custom_colors,zorder=2)
        finally:
            
            # setze xlim zurück
            ax.set_xlim((left,right))

            # Erstelle einen Kasten mit weiteren Infos im Diagramm
            if infos == True:
                at = self.AnchoredText(f'Achsenabschnitt: {self.n_val} $\pm$ {self.n_err} \n Steigung: {self.m_val} $\pm$ {self.m_err}',
                loc=self.textloc,prop=dict(size=self.ANCH))
                ax.add_artist(at)
            if legend == True:
                #---Löscht Fehlerbalken aus Legende---
                handles, labels = ax.get_legend_handles_labels()
                handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]

                ax.legend(handles, labels,frameon=True,prop={'size': self.legendsize})

            if name != '':
                plt.savefig(name,dpi=self.dpi)
                print('Datei gespeichert')
                
                with open('data.tex','a') as file:
                    figure = '\\begin{figure}\n    \\centering\n    \includegraphics[width=\linewidth]{'+name+'}\n\\end{figure}\n'
                    file.write(figure)

            plt.show()
            return self

    # kann manuell zusätzlichen Plot hinzufügen
    custom_plot_x = 0
    custom_plot_y = 0
    custom_multi_array = 0
    custom_label = ['label']
    custom_colors = ['tab:green','tab:purple','tab:orange']
    def add_plot(self,x,y,label = '',colors = ''):
        if np.shape(x) == np.shape(y):
        
            if label != '':
                self.custom_label = label

            if colors != '':
                self.custom_colors = colors

            try:
                self.custom_plot_x = np.transpose(np.array(x))
                self.custom_plot_y = np.transpose(np.array(y))
            except:
                print('add_plot error')

            try:
                self.custom_multi_array = np.shape(self.custom_plot_x)[1]
                if label == '':
                    self.custom_label = ['label'] * self.custom_multi_array
            except:
                if colors == '':
                    self.custom_colors = 'tab:green'
                return
        else:
            print('x und y müssen diesselben Dimensionen haben')


#-------------------------------------------------------------------------------------------
#--------------------FÜGE-MEHRERE-GRAPPHEN-IM-SELBEN-DIAGRAMM-EIN---------------------------
#-------------------------------------------------------------------------------------------
class multiplot():
    
    # Style des Diagramms
    style = ['grid','default']
    try:
        style = ['grid','notebook','science']
    except:
        style = ['grid','default']
    
    size = 20
    def _size(self):
        BIG = self.size 
        SMALL = self.size * 0.5
        MID = self.size * 0.75
        plt.rc('font', size=MID)          # controls default text sizes
        plt.rc('axes', titlesize=BIG)     # fontsize of the axes title
        plt.rc('axes', labelsize=MID)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL)    # legend fontsize
        plt.rc('figure', titlesize=BIG)  # fontsize of the figure title

    # Dies werden später Arrays sein von Steigung m, Achsenabschnitt n, x- und y Werte sowie ihre Fehler
    m, merr, n, nerr, x, y, xerr, yerr = 0, 0 ,0 ,0 ,0, 0, 0, 0

    # Anzahl der Plots
    num = 0

    # standard farbenfolge für Fehlerbalken
    color = ['tab:blue','tab:green','tab:red','tab:purple','tab:cyan'] 

    # Definiere Variable für die Label der Graphen
    label = ['label']

    # Setze Anzahl der Plots, damit die Funktion die Arraygrößen definieren kann
    def plotcount(self, num):
        self.m = np.zeros(num)
        self.merr = np.zeros(num)
        self.n = np.zeros(num)
        self.nerr = np.zeros(num)
        self.x = [0]*num
        self.y = [0]*num
        self.xerr = [0]*num
        self.yerr = [0]*num
        self.num = num
        self.label = ['label'] * num
        self.shapes = ['o'] * num 

        return

    # Setze die Werte der einzelnen Fits in die Arrays an der Stelle i ein
    def set_result(self,result,i):
        self.m[i] = result['m']
        self.merr[i] = result['merr']
        self.n[i] = result['n']
        self.nerr[i] = result['nerr']
        self.x[i] = result['x_vals']
        self.y[i] = result['y_vals']
        self.yerr[i] = result['yerr']

        return result

    # Gibt die Ergbenisse als Arrays aus
    def _print_results(self):
        title = ['Plot ', 'Steigung m', 'm-Fehler','Abschnitt n', 'n-Fehler']
        print(title)
        

        # Eine Liste, die mit allen Werten zur Ausgabe gefüllt wird
        lst = [] 

        werte = [self.label, self.m, self.merr, self.n ,self.nerr]
        vals = np.zeros(shape=(self.num,4))

        for i in range(self.num):
            row = []
            for j,m in enumerate(werte):
                row.append(m[i])
                if j != 0:
                    vals[i,j-1] = m[i]
            lst.append(row)

        
        for i in range(self.num):
            print(self.label[i], vals[i])
        
        


    # Mathematische Funktion der Form F(x):=mx+n
    def __f(self,x,m,n):
        return x*m+n

    errbar = [5,5,1,1] # marker, caps, eline, markerwidth
    shapes = ['o']

    # die Variablen der Limits des Diagramms
    ylim = (0,0)
    xlim = (0,0)

    # Setze die Ticks der Achsen
    xticks = 0
    yticks = 0
    
    # Rotation der Achsenbeschriftung
    xrotation = 0
    yrotation = 0

    plotsize = (6,4)
    dpi = 300


    # Plotte alle Fits
    def plot(self,title='title',xlabel='x_Achse',ylabel='y_achse',name='',hide=False):

        #Gibt Ergebnisse aus
        self._print_results()

        # Erstellt das Diagramm
        plt.style.use('default') # verhindert, dass Fehler bei der Anzeige entstehen
        plt.style.use(self.style)
        self._size()

        plt.rcParams['figure.dpi'] = 120
        fig, ax = plt.subplots(figsize=self.plotsize)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        
        if self.ylim != (0,0):
            ax.set_ylim(self.ylim)
        if self.xlim != (0,0):
            ax.set_xlim(self.xlim)
        
        #setze die ticks der achsen
        try:
            if self.xticks != 0:
                plt.xticks(self.xticks)
            if self.yticks != 0:
                plt.yticks(self.yticks)
        except:
            print('error: konnte nicht ticks setzen')

        ax.tick_params(axis='x', labelrotation=self.xrotation)
        ax.tick_params(axis='y', labelrotation=self.yrotation)

        # Plotte mit for-schleife alle Fits
        for i in range(self.num):
            #ax.plot(self.x[i], self.__f(self.x[i],self.m[i],self.n[i]),'--',color=self.color[i%len(self.color)], alpha=0.75)
            ax.errorbar(self.x[i], self.y[i],marker=self.shapes[i],ms=self.errbar[0],ls='',color=self.color[i%len(self.color)],
            yerr=self.yerr[i],label=self.label[i],capsize=self.errbar[1], elinewidth=self.errbar[2],
            markeredgewidth=self.errbar[3])
        
        left, right = ax.get_xlim()
        x_axis = np.linspace(left,right,10)

        if hide == False:
            for i in range(self.num):
                ax.plot(x_axis, self.__f(x_axis,self.m[i],self.n[i]),'--',color=self.color[i%len(self.color)], alpha=0.75)

        ax.set_xlim((left,right))


        ax.legend(bbox_to_anchor=(1.01, 1),frameon=True,fontsize=12)

        if name != '':
            plt.savefig(name,dpi=self.dpi)
            print('Datei gespeichert')

            with open('data.tex','a') as file:
                figure = '\\begin{figure}\n    \\centering\n    \includegraphics[width=\linewidth]{'+name+'}\n\\end{figure}\n'
                file.write(figure)

        plt.show()
    
        return self