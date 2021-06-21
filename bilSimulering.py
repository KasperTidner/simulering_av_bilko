import random
import matplotlib.pyplot as plt
import tkinter as tk

#Konstanter
"""------------------------------------------------------------------------"""
vägLängd = 1000 #längden på vägen (meter)
q1 = 0 #avstånd från vägens början till det synliga simuleringsområdets början
q3 = 1000 #avstånd från vägens början till det synliga simuleringsområdets slut
maxTid = 900
"""------------------------------------------------------------------------"""

#Listor
"""------------------------------------------------------------------------"""
bilarLista = [] #Lista som innehåller alla bilar
passeradeBilarLista = [] #Lista som innehåller hur många bilar som passerat per minut
"""------------------------------------------------------------------------"""

#Föränderliga variabler via GUI
"""------------------------------------------------------------------------"""
class GraphicUserInterface(tk.Frame):
    """Skapar en GUI där användaren kan på ett interaktivt sätt ändra varibel värden """
    
    def __init__(self, master=None):
        """Skapar en interaktiv ruta """
        
        super().__init__(master)
        self.master = master
        self.master.title("Simulering")
        self.pack()
        self.skapaWidgets()

    def skapaWidgets(self):
        """Skapar alla interaktiva Widgetar"""
        
        #Titel
        self.labelTitel = tk.Label(self)
        self.labelTitel["text"] = "Simulering av trafikflöde"
        self.labelTitel["font"] = ("Arial", 35)
        self.labelTitel.grid(row=0, column=0, rowspan=1, columnspan=5)
                
        #Radbrytare
        self.radBryt1 = tk.Label(self)
        self.radBryt1["pady"] = 3
        self.radBryt1.grid(row=1, column=0, rowspan=1, columnspan=5)         
        
        #Slider för antalet bilar
        self.sliderAntalBilar = tk.Scale(self)
        self.sliderAntalBilar["from_"] = 0
        self.sliderAntalBilar["to"] = 400
        self.sliderAntalBilar["tickinterval"] = 25
        self.sliderAntalBilar["resolution"] = 1
        self.sliderAntalBilar["length"] = 700
        self.sliderAntalBilar["bd"] = 3
        self.sliderAntalBilar["orient"] = tk.HORIZONTAL
        self.sliderAntalBilar["label"] = "Antal bilar"
        self.sliderAntalBilar.set(40)
        self.sliderAntalBilar.grid(row=2, column=0, rowspan=1, columnspan=5)
                
        #Radbrytare
        self.radBryt2 = tk.Label(self)
        self.radBryt2["pady"] = 3
        self.radBryt2.grid(row=3, column=0, rowspan=1, columnspan=5) 
                
        #Slider för hastighetsgränsen
        self.sliderHastighet = tk.Scale(self)
        self.sliderHastighet["from_"] = 30
        self.sliderHastighet["to"] = 120
        self.sliderHastighet["tickinterval"] = 10
        self.sliderHastighet["resolution"] = 10
        self.sliderHastighet["length"] = 700
        self.sliderHastighet["bd"] = 3
        self.sliderHastighet["orient"] = tk.HORIZONTAL
        self.sliderHastighet["label"] = "Fartgräns"
        self.sliderHastighet.set(80)
        self.sliderHastighet.grid(row=4, column=0, rowspan=1, columnspan=5)
                
        #Radbrytare
        self.radBryt3 = tk.Label(self)
        self.radBryt3["pady"] = 3
        self.radBryt3.grid(row=5, column=0, rowspan=1, columnspan=5)         
        
        #Slider för antalet filer
        self.sliderAntalFiler = tk.Scale(self)
        self.sliderAntalFiler["from_"] = 1
        self.sliderAntalFiler["to"] = 8
        self.sliderAntalFiler["tickinterval"] = 1
        self.sliderAntalFiler["resolution"] = 1
        self.sliderAntalFiler["length"] = 700
        self.sliderAntalFiler["bd"] = 3
        self.sliderAntalFiler["orient"] = tk.HORIZONTAL
        self.sliderAntalFiler["label"] = "Antal filer"
        self.sliderAntalFiler.set(3)
        self.sliderAntalFiler.grid(row=6, column=0, rowspan=1, columnspan=5)        
        
        #Radbrytare
        self.radBryt4 = tk.Label(self)
        self.radBryt4["pady"] = 3
        self.radBryt4.grid(row=7, column=0, rowspan=1, columnspan=5) 
                
        #Slider för deltasekunder, tidsstegen i simuleringen
        self.sliderTidSteg = tk.Scale(self)
        self.sliderTidSteg["from_"] = 0
        self.sliderTidSteg["to"] = 2
        self.sliderTidSteg["tickinterval"] = 1
        self.sliderTidSteg["resolution"] = 0.2
        self.sliderTidSteg["length"] = 700
        self.sliderTidSteg["bd"] = 3
        self.sliderTidSteg["orient"] = tk.HORIZONTAL
        self.sliderTidSteg["label"] = "Tidssteg (sekunder)"
        self.sliderTidSteg.set(1)
        self.sliderTidSteg.grid(row=8, column=0, rowspan=1, columnspan=5)        
        
        #Radbrytare
        self.radBryt5 = tk.Label(self)
        self.radBryt5["pady"] = 3
        self.radBryt5.grid(row=9, column=0, rowspan=1, columnspan=5) 
                
        #Titel hinder på vägen
        self.labelHinderExisterar = tk.Label(self)
        self.labelHinderExisterar["text"] = "Tillåt hinder?"
        self.labelHinderExisterar.grid(row=10, column=0, rowspan=1, columnspan=1)
        
        #Knapp hinder på vägen
        self.buttonHinderExisterar = tk.Button(self)
        self.buttonHinderExisterarState = False
        self.buttonHinderExisterar["text"] = "False"
        self.buttonHinderExisterar["fg"] = "red"
        self.buttonHinderExisterar["command"] = self.toggleButtonHinderExisterar
        self.buttonHinderExisterar.grid(row=11, column=0, rowspan=1, columnspan=1)        
        
        #Titel tillåt filbyten
        self.labelTillåtFilbyten = tk.Label(self)
        self.labelTillåtFilbyten["text"] = "Tillåt filbyten?"
        self.labelTillåtFilbyten.grid(row=10, column=1, rowspan=1, columnspan=1)
        
        #Knapp tillåt filbyten
        self.buttonTillåtFilbyten = tk.Button(self)
        self.buttonTillåtFilbytenState = True
        self.buttonTillåtFilbyten["text"] = "True"
        self.buttonTillåtFilbyten["fg"] = "green"
        self.buttonTillåtFilbyten["command"] = self.toggleButtonTillåtFilbyten
        self.buttonTillåtFilbyten.grid(row=11, column=1, rowspan=1, columnspan=1)
                
        #Titel slumpmässig bromsning
        self.labelSlumpBromsning = tk.Label(self)
        self.labelSlumpBromsning["text"] = "Tillåt slumpmässig bromsning?"
        self.labelSlumpBromsning.grid(row=10, column=2, rowspan=1, columnspan=1)
        
        #Knapp slumpmässig bromsning
        self.buttonSlumpBromsning = tk.Button(self)
        self.buttonSlumpBromsningState = True
        self.buttonSlumpBromsning["text"] = "True"
        self.buttonSlumpBromsning["fg"] = "green"
        self.buttonSlumpBromsning["command"] = self.toggleButtonSlumpBromsning
        self.buttonSlumpBromsning.grid(row=11, column=2, rowspan=1, columnspan=1)        
        
        #Titel simulera med modulo
        self.labelModuloSimulering = tk.Label(self)
        self.labelModuloSimulering["text"] = "Simulera vilken del av kön?"
        self.labelModuloSimulering.grid(row=10, column=3, rowspan=1, columnspan=1)
        
        #Knapp simulera med modulo
        self.buttonModuloSimulering = tk.Button(self)
        self.buttonModuloSimuleringState = True
        self.buttonModuloSimulering["text"] = "Mitten"
        self.buttonModuloSimulering["fg"] = "black"
        self.buttonModuloSimulering["command"] = self.toggleButtonModuloSimulering
        self.buttonModuloSimulering.grid(row=11, column=3, rowspan=1, columnspan=1) 
        
        #Titel skapa animation
        self.labelSkapaAnimation = tk.Label(self)
        self.labelSkapaAnimation["text"] = "Skapa animation?"
        self.labelSkapaAnimation.grid(row=10, column=4, rowspan=1, columnspan=1)
        
        #Knapp skapa animatiom
        self.buttonSkapaAnimation = tk.Button(self)
        self.buttonSkapaAnimationState = False
        self.buttonSkapaAnimation["text"] = "False"
        self.buttonSkapaAnimation["fg"] = "red"
        self.buttonSkapaAnimation["command"] = self.toggleButtonSkapaAnimation
        self.buttonSkapaAnimation.grid(row=11, column=4, rowspan=1, columnspan=1) 
        
        #Radbrytare
        self.radBryt6 = tk.Label(self)
        self.radBryt6["pady"] = 3
        self.radBryt6.grid(row=12, column=0, rowspan=1, columnspan=5)         
        
        #Kör simulering
        self.buttonKör = tk.Button(self)
        self.buttonKör["text"] = "Kör simulering"
        self.buttonKör["command"] = self.runProgram
        self.buttonKör.grid(row=13, column=0, rowspan=1, columnspan=5)        
        
        #Radbrytare
        self.radBryt7 = tk.Label(self)
        self.radBryt7["pady"] = 3
        self.radBryt7.grid(row=14, column=0, rowspan=1, columnspan=5)    
        
    def toggleButtonHinderExisterar(self):
        """Funktionen växlar statusen på knappen, byter mellan att sätta på / stänga av hinder"""
        
        self.buttonHinderExisterarState = not self.buttonHinderExisterarState
        
        if self.buttonHinderExisterarState:
            self.buttonHinderExisterar.config(text="True", fg='green')
        else:
            self.buttonHinderExisterar.config(text="False", fg='red')
                
    def toggleButtonTillåtFilbyten(self):
        """Funktionen växlar statusen på knappen, byter mellan att sätta på / stänga av filbyten"""
        
        self.buttonTillåtFilbytenState = not self.buttonTillåtFilbytenState
        
        if self.buttonTillåtFilbytenState:
            self.buttonTillåtFilbyten.config(text="True", fg='green')
        else:
            self.buttonTillåtFilbyten.config(text="False", fg='red')
             
    def toggleButtonSlumpBromsning(self):
        """Funktionen växlar statusen på knappen, byter mellan att sätta på / stänga av slumpmässig bromsning"""
        
        self.buttonSlumpBromsningState = not self.buttonSlumpBromsningState
        
        if self.buttonSlumpBromsningState:
            self.buttonSlumpBromsning.config(text="True", fg='green')
        else:
            self.buttonSlumpBromsning.config(text="False", fg='red')
            
    def toggleButtonModuloSimulering(self):
        """Funktionen växlar statusen på knappen, byter mellan att simulera i mitten / slutet av kön"""
        
        self.buttonModuloSimuleringState = not self.buttonModuloSimuleringState
        
        if self.buttonModuloSimuleringState:
            self.buttonModuloSimulering.config(text="Mitten", fg='black')
        else:
            self.buttonModuloSimulering.config(text="Slutet", fg='black')
    
    def toggleButtonSkapaAnimation(self):
        """Funktionen växlar statusen på knappen, byter mellan att sätta på / stänga av animeringen"""
        
        self.buttonSkapaAnimationState = not self.buttonSkapaAnimationState
        
        if self.buttonSkapaAnimationState:
            self.buttonSkapaAnimation.config(text="True", fg='green')
        else:
            self.buttonSkapaAnimation.config(text="False", fg='red')
        
    def runProgram(self):
        """Funktionen samlar in alla värden från GUIn och anropar sedan main funktionen"""
        
        self.antalBilar = self.sliderAntalBilar.get()
        self.tillåtenHastighet = self.sliderHastighet.get()
        self.antalFiler = self.sliderAntalFiler.get()
        self.deltaTid = self.sliderTidSteg.get()
        
        
        #Ser till så att antal bilar är större än 0, så att programmet går att köra.
        if self.antalBilar == 0:
            self.antalBilar = 50
        
        #Ser till så att deltaTid är större än 0, så att programmet går att köra.
        if self.deltaTid == 0:
            self.deltaTid = 1
            
        self.tillåtHinder=self.buttonHinderExisterarState
        self.tillåtFilbyten = self.buttonTillåtFilbytenState
        self.tillåtSlumpBroms = self.buttonSlumpBromsningState
        self.moduloSimulering = self.buttonModuloSimuleringState
        self.moduloSimuleringText =  self.buttonModuloSimulering["text"]
        self.skapaAnimation = self.buttonSkapaAnimationState
    
        main()
"""------------------------------------------------------------------------"""

class Bilar:
    """ Klassen håller inne alla bilars värden och egenskaper, samt funktioner för att uppdatera dessa"""
  
    def __init__(self, x, fil, hastighet):
        """Skapar bilarna"""
        
        self.x = x
        self.fil = fil
        self.maxHastighet = hastighet #Hastigheten man vill nå upp till
        self.nuvarandeHastighet = self.maxHastighet #Hastigheten man kör i
        self.r, self.g, self.b = self.färg()
        self.färg = (self.r, self.g, self.b)
        self.senastByteVänster = 0
        self.senastByteHöger = 0
          
    def färg(self):
        """ En funktion som tilldelar bilar en färg efter hastigheten de vill köra, på en linjärskala från högsta hastighet(röd) till lägsta hastighet(grön)"""
        
        mu = 0.986*gui.tillåtenHastighet + 10.77 #Linjärt anpassat mönster för normalfördelade medelvärden på hastigheter
        sigma = 0.037*gui.tillåtenHastighet + 3.3 #Linjärt anpassat mönster för normalfördelade standardavvikelser på hastigheter
        rangeFärg = 2*sigma
        
        #Skapar en svart punkt om max hastigheten är 0 (hinder)
        if self.maxHastighet == 0:
            r = 0
            g = 0
            b = 0
        
        #Tilldelar punkterna som är långsammare än medelvärdet grönare nyanser ju långsamare de är
        elif self.maxHastighet <= mu:
            r = int(255*(1-(mu-self.maxHastighet)/rangeFärg))
            g = 255
            b = 0
            if r < 0:
                r = 0
        
        #Tilldelar punkterna som är snabbare än medelvärdet rödare nyanser desto snabbare de är
        else:
            r = 255
            g = int(255*(1-(self.maxHastighet-mu)/rangeFärg))
            b = 0
            if g < 0:
                g = 0
        
        #Gör färgerna intill läsliga rgb andelar.
        r = r/255
        g = g/255
        b = b/255
        
        return r,g,b
            
    def iKappKörning(self, simuleradTid):
        """beräknar avstånd till bilen framför och avgör om man är för nära, och i så fall om man ska bromsa eller byta fil för att köra om """
    
        #Storerar ut alla bilar som ligger före bilen i samma fil och loopar igenom dem för att hitta den närmaste bilen
        sammaFil = [(bilFramför.x, bilFramför.nuvarandeHastighet, bilFramför.maxHastighet, bilFramför.fil) for bilFramför in bilarLista if (bilFramför.fil==self.fil and bilFramför.x > self.x)] 
        
        #Räknar ut den närmaste bilen framför i samma fil
        try:
            närmastBil = sammaFil[0]
            for bilFramför in sammaFil:
                (xBilFramför, hastBilFramför, maxHastBilFramför, filBilFramför) = bilFramför
                if xBilFramför < närmastBil[0]:
                    närmastBil = bilFramför
            
            (xBilFramför, hastBilFramför, maxHastBilFramför, filBilFramför) = närmastBil
            
        #Om det inte finns en bil framför i samma fil, så tittas vilken som är den närmaste bilen enligt modulo, annars accelerera
        except IndexError:
            
            #Om modulo är påslaget, så kollas vilken bil som har det lägsta x värdet och så antas dens x värde öka med vägLängden så att den nu ligger framför bilen
            if gui.moduloSimulering == True:
                sammaFilModulo = [(bilFramför.x, bilFramför.nuvarandeHastighet, bilFramför.maxHastighet, bilFramför.fil) for bilFramför in bilarLista if (bilFramför.fil==self.fil and bilFramför.x != self.x)]
                
                try:
                    närmastBil = sammaFilModulo[0]
                    for bilFramför in sammaFilModulo:
                        (xBilFramför, hastBilFramför, maxHastBilFramför, filBilFramför) = bilFramför
                        if xBilFramför < närmastBil[0]:
                            närmastBil = bilFramför
                    
                    (xBilFramför, hastBilFramför, maxHastBilFramför, filBilFramför) = närmastBil
                    
                    #Ändrar bilen framförs x värde med väglängden (kongurent i modulo väglängd).
                    xBilFramför += vägLängd
                
                #Om ingen bil finns i samma fil, så accelerar och avbryt funktionen
                except IndexError:
                    self.accelerera()
                    return
            
            #Om modulo är av så accelererar man om man inte har en bil framför.
            else:
                self.accelerera()
                return

        #Tittar om bilen är inom avståndet av två sekunder (folk håller inte tre sekunders regeln)
        if xBilFramför - self.x > 0 and xBilFramför - self.x <= 2*self.nuvarandeHastighet/3.6:
        
            #Sorterar ut alla bilar i filen till vänster för att se om ett filbyte är möjligt
            vänsterFil = [bilVänster.x for bilVänster in bilarLista if bilVänster.fil==(self.fil+1)]
            for xBilVänster in vänsterFil:
            
                #Om en bil ligger för nära i filen till vänster så bromsar man istället, bromsningen beror på hur nära man ligger bilen framför
                if abs(xBilVänster - self.x) <= 1*self.nuvarandeHastighet/3.6 or (simuleradTid - self.senastByteHöger) < 10 or self.maxHastighet < maxHastBilFramför:
                    self.bromsa(xBilFramför, hastBilFramför)
                    return
                
            #Om ingen bil ligger i vägen i filen till vänster så kollar man om det faktiskt finns en fil till vänster samt om filbyte är tillåtet, om nej, så bromsar man 
            if self.fil == gui.antalFiler or gui.tillåtFilbyten == False:
                self.bromsa(xBilFramför, hastBilFramför)
                return
            
            #Om man har en fil till vänster och ett filbyte är möjligt så byter man fil
            else:
                self.fil += 1
                self.senastByteVänster = simuleradTid
                return
        
        #Om den närmaste bilen inte ligger inom tre sekunders avståndet så accelererar man.
        else:
            self.accelerera()
            return
    
    def bromsa(self, xBilFramför, hastBilFramför):
        """Bromsar bilarna beroende på avståndet till bilen framför"""
        
        if xBilFramför - self.x > 0 and xBilFramför - self.x <= 8: #Varje bil är igenomsnitt 5m och minsta avståndet mellan två bilar i kö ca 3m
            self.nuvarandeHastighet = 0
        elif xBilFramför - self.x > 0 and xBilFramför - self.x <= 1*self.nuvarandeHastighet/3.6:
            self.nuvarandeHastighet = hastBilFramför*0.5
        elif xBilFramför - self.x > 0 and xBilFramför - self.x <= 2*self.nuvarandeHastighet/3.6:
            self.nuvarandeHastighet = hastBilFramför*0.7
        elif xBilFramför - self.x > 0 and xBilFramför - self.x <= 3*self.nuvarandeHastighet/3.6: 
            self.nuvarandeHastighet = hastBilFramför*0.9
    
    
    def bytaFilHöger(self, simuleradTid):
        """ Byter fil mot höger om det går"""
        
        #Om filbyte är tillåtet och om man inte ligger i innersta filen, samt om man just inte har bytt fil åt vänster för att köra om, så finns en chans för att byta fil.
        if gui.tillåtFilbyten == True and self.fil >= 2 and (simuleradTid - self.senastByteVänster) > 10:
            mu = 0.986*gui.tillåtenHastighet + 10.77 #Linjärt anpassat mönster för normalfördelade medelvärden på hastigheter
            sigma = 0.037*gui.tillåtenHastighet + 3.3 #Linjärt anpassat mönster för normalfördelade standardavvikelser på hastigheter
            
            #Räknar ut sanolikheten för att byta fil linjärt, 0 för snabbaste bilen och 0,2 för långsamaste
            högerFilByteSannolikhet = (abs(self.maxHastighet - (mu+3*sigma))/(6*sigma))/5
            
            #För att efterlikna verkligheten mer så får snabba bilar än ännu mindre sannolikhet att byta, och långsamma bilar än ännu större.
            if högerFilByteSannolikhet <= 0.08:
                högerFilByteSannolikhet /= 4
            elif högerFilByteSannolikhet >= 0.13:
                högerFilByteSannolikhet *= 2
            
            #Kollar sen om det finns en bil ivägen i höger filen, om det finns avbryt försöket
            högerFil = [bilHöger.x for bilHöger in bilarLista if bilHöger.fil==(self.fil-1)]
            for xBilHöger in högerFil:
                if abs(xBilHöger - self.x) <= 1*self.nuvarandeHastighet/3.6:
                    return
            
            #Annars byt fil slumpmässig med en sannolikhet kopplad till bilens hastighet
            if random.random() < högerFilByteSannolikhet:
                self.fil -= 1
                self.senastByteHöger = simuleradTid
                
    def accelerera(self):
        """ Gör acceleraionen """
        
        #Om man är långsammare än sin max hastighet så ökas farten med 5% av max hastigheten
        if self.nuvarandeHastighet < self.maxHastighet:
            self.nuvarandeHastighet += self.maxHastighet/20
        
        #Om nuvarandehastigheten nu överstiger max hastigheten, så nollställs nuvarande hastigheten till max
        if self.nuvarandeHastighet > self.maxHastighet:
            self.nuvarandeHastighet = self.maxHastighet
                
    def slumpBromsning(self):
        "Slumpmässigt bromsar bilar"
        
        #Bromsar en bil slumpmässigt med 0,1% sannolikhet
        if random.random() < 0.01:
            self.nuvarandeHastighet *= 0.6
            
def bilskapare():
    """skapar en lista med bilarna som objekt i klassen Bilar"""
    
    #Skapar anatlet bilar som specifierats i GUIn, värden slumpas ut 
    for bil in range(gui.antalBilar):
        x = random.randrange(0, vägLängd, 1)
        fil = random.randrange(1, gui.antalFiler+1, 1)
        hastighet = tilldelaHastighet()
        bilarLista.append(Bilar(x, fil, hastighet))
    
    #Om hinder är påslaget skapas en bil utan hastighetn som är stillastående i höger filen
    if gui.tillåtHinder == True:
        bilarLista.append(Bilar(int(0.75*vägLängd), 1, 0))
                
def tilldelaHastighet():
    """tilldelar bilarna olika hastigheter från en normalfördelad kurva."""
    
    mu = 0.986*gui.tillåtenHastighet + 10.77 #Linjärt anpassat mönster för normalfördelade medelvärden på hastigheter
    sigma = 0.037*gui.tillåtenHastighet + 3.3 #Linjärt anpassat mönster för normalfördelade standardavvikelser på hastigheter
    normalFördeladHastighet = random.normalvariate(mu, sigma)
    
    return normalFördeladHastighet

def uppdateraBilar(simuleradTid, passeradeBilar):
    """loopar igenom listan med alla bilar i och uppdaterar deras värden(x, fil och hastighet) """
    
    #Går igenom varje bil och jämför med bilar framför
    for bil in bilarLista:
        bil.iKappKörning(simuleradTid) # bil.fil, bil.nuvarandeHastighet =
        
        #Nollställer hastigheten till max om man överstigit den hastigheten man högst känner sig bekvm att köra
        if bil.nuvarandeHastighet > bil.maxHastighet:
            bil.nuvarandeHastighet = bil.maxHastighet
        
        #Om slumpmässig bromsning är tillåten så slumpas det om en bil bromsar oväntat eller inte.
        if gui.tillåtSlumpBroms == True:
            bil.slumpBromsning()
            
        #Uppdaterar bilen x-position och nollställer den om man lämnat simulerings området
        bil.x += bil.nuvarandeHastighet/3.6 * gui.deltaTid     
        if bil.x >= vägLängd:
            bil.x = 0
            
            #Håller räkningen på antalet bilar som passerat simuleringsområdets yttregräns och blivit nollställda
            passeradeBilar += 1
            
        #Provar att byta mot en inre fil.
        bil.bytaFilHöger(simuleradTid)
            
    return passeradeBilar
                          
def plottaSimulering(simuleradTid):
    """gör själva plottarna av bilarna. Denna funktion använder några av funktionerna ovan. """
    
    plt.figure()
    plt.axes(xlim=(q1, q3), ylim=(0, gui.antalFiler+1))
    
    #Skriver ut den simulerade tiden
    text = "Simulerad tid: " + str(simuleradTid) + "s."
    plt.title(text)
    
    #Skapar vägmarkeringarna
    plt.plot([q1, q3], [0.5, 0.5], 'k-', lw=2)
    plt.plot([q1, q3], [gui.antalFiler+0.5, gui.antalFiler+0.5], 'k-', lw=2)
    for line in range(q1,q3,int(vägLängd/40)):
        for lane in range(1, gui.antalFiler):
            plt.plot([int(line+(vägLängd/160)), int(line+(vägLängd/40)-(vägLängd/160))], [lane+0.5, lane+0.5], 'k-', lw=2)
    
    #Plottar bilarna
    for bil in bilarLista:    
        plt.scatter(bil.x, bil.fil, color=bil.färg)
    plt.show()

def startUtskrift():
    """Skriver en utskrift i början med information om simuleringen"""
    
    print("\n\nSimuleringen är startad!")
    print("\nInput värden:")
    print("-----------------------")
    print("Antal bilar: " + str(gui.antalBilar))
    print("Hastighet: " + str(gui.tillåtenHastighet))
    print("Antal filer: " + str(gui.antalFiler))
    print("dT: " + str(gui.deltaTid))
    print("Hinder: " + str(gui.tillåtHinder))
    print("Filbyten: " + str(gui.tillåtFilbyten))
    print("Slump bromsning: " + str(gui.tillåtSlumpBroms))
    print("Del av kön: " + str(gui.moduloSimuleringText))
    print("Skapa animation: " + str(gui.skapaAnimation) + "\n")
    print("\nSimuleringskod: " + str(gui.tillåtenHastighet) + str(gui.antalFiler) + str(gui.tillåtHinder)[0] + str(gui.tillåtFilbyten)[0] + str(gui.tillåtSlumpBroms)[0] + str(gui.moduloSimuleringText)[0])

def dataUtskrift(simuleradTid, passeradeBilar, procent):
    """Skriver ut data om trafikflödet varje minut """
    
    print("\n\n------------------------------------------------------------------")
    print("Trafikdensitet: " + str(round(gui.antalBilar/((vägLängd/1000)*gui.antalFiler), 3)) + " bilar per km")
    print("Trafikflödet mellan " + str(simuleradTid-60) + " - " + str(simuleradTid) + ": " + str(passeradeBilar) + " bilar per minut")
    print("Hastighet: " + str(round(procent, 2)) + "% av max")
    print("\nSimuleringskod: " + str(gui.tillåtenHastighet) + str(gui.antalFiler) + str(gui.tillåtHinder)[0] + str(gui.tillåtFilbyten)[0] + str(gui.tillåtSlumpBroms)[0] + str(gui.moduloSimuleringText)[0])
    print()
    
def slutUtskrift(simuleradTid, passeradeBilarLista):
    """Skriver ut data om trafikflödet varje minut """
    
    trafikflöde = 0
    hastighet = 0
    for data in passeradeBilarLista:
        trafikflöde += data[1]
        hastighet += data[2]
    
    trafikflöde /= (simuleradTid / 60)
    hastighet /= (simuleradTid / 60)
    totalTid = simuleradTid
    
    print("\n\n------------------------------------------------------------------")
    print("Simulering sluförd!\n")
    print("\nInput värden:")
    print("-----------------------")
    print("Hastighet: " + str(gui.tillåtenHastighet))
    print("Antal filer: " + str(gui.antalFiler))
    print("dT: " + str(gui.deltaTid))
    print("Hinder: " + str(gui.tillåtHinder))
    print("Filbyten: " + str(gui.tillåtFilbyten))
    print("Slump bromsning: " + str(gui.tillåtSlumpBroms))
    print("Del av kön: " + str(gui.moduloSimuleringText))
    print("Skapa animation: " + str(gui.skapaAnimation) + "\n")
    print("Resultat:")
    print("-----------------------")
    print("Total simulerad tid: " + str(totalTid) + "sekunder")
    print("Trafikdensitet: " + str(round(gui.antalBilar/((vägLängd/1000)*gui.antalFiler), 3)) + " bilar per km")
    print("Medel trafikflöde: " + str(round(trafikflöde, 2)) + " bilar per minut")
    print("Genomsnittlig hastighet av max: " + str(round(hastighet, 2)) + "%")
    print("Rawdata: " + str(passeradeBilarLista))
    print("\nSimuleringskod: " + str(gui.tillåtenHastighet) + str(gui.antalFiler) + str(gui.tillåtHinder)[0] + str(gui.tillåtFilbyten)[0] + str(gui.tillåtSlumpBroms)[0] + str(gui.moduloSimuleringText)[0] + "\n\n")

    
def main():
    """Huvudfunktionen som kör alla andra funktioner """
    
    #Skriver ut inställningar för simulationen
    startUtskrift()
    
    #Nollställer värden och skapar nya bilar
    simuleradTid = 0 #Tid som gått i simuleringen (sekunder)
    passeradeBilar = 0 #Bilar som passerat en viss punkt
    procent = 0 
    passeradeBilarLista.clear()
    bilarLista.clear()
    bilskapare()
    
    #Simuleringstid
    while simuleradTid<maxTid:
        
        #Plottar simuleringen, uppdaterar bilarna, och sen uppdaterar tiden
        if gui.skapaAnimation == True:
            plottaSimulering(simuleradTid)
            
        passeradeBilar = uppdateraBilar(simuleradTid, passeradeBilar)
        simuleradTid += gui.deltaTid
        
        #Om en minut har gått, räkna ihop trafikflödet och den genomsnittliga hastigheten och för in det i data listan, samt gör en utskrift
        if simuleradTid % 60 == 0:
            for i in range(0, gui.antalBilar):
                procent += round(bilarLista[i].nuvarandeHastighet / bilarLista[i].maxHastighet *100, 2)
            procent /= gui.antalBilar
            
            passeradeBilarLista.append((simuleradTid, passeradeBilar, procent))
            
            #Skriver ut data
            dataUtskrift(simuleradTid, passeradeBilar, procent)
            
            #Nollställer data
            passeradeBilar = 0
            procent = 0
    
    #Skriver ut data över simulationen
    slutUtskrift(simuleradTid, passeradeBilarLista)
            
root = tk.Tk()
gui = GraphicUserInterface(master=root)
gui.mainloop()