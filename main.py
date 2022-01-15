import kivy

import datetime
 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

import os

class antigos(BoxLayout):
    def __init__(self,text = '',**kwargs):
        super().__init__(**kwargs)
        self.ids.valor_antigo.text = text
        self.text = text

class proximos(Button):
    def __init__(self,text = '',**kwargs):
        super().__init__(**kwargs)
        self.text = text


class box(BoxLayout):

    local_aplicacao = ''
    def __init__(self):
        super().__init__()


        if 'aplicados' not in os.listdir():
            arq = open('aplicados','w'); arq.close()
            arq = open('adiantados','w'); arq.close()
        self.abre_antigos()
        self.local_aplicacao_func()
        self.adiantado = False


    def abre_antigos(self):
        dic = {0:'Segunda',1:'Terça',2:'Quarta',3:'Quinta',
               4:'Sexta',5:'Sábado',6:'Domingo'}
        
        self.lista = [11,19,17,10,25,3,21,6,20,24,7,4,
                      26,5,23,2,9,22,18,28,8,1]
        
        self.lista_original = self.lista.copy()
        

        
        arq = open('aplicados')
        lista_textos = []
        for i in arq.readlines():
            i = i.split()
            numero = i[0]
            if numero[0] == '0':
                numero = eval(numero[1:])
            else:
                numero = eval(numero)

            dt = datetime.datetime(*eval(i[1]))
            if dt.hour <= 6:
                dt = dt - datetime.timedelta(1)
            texto = '%s - %s/%s/%s - %s'%(numero,dt.day,dt.month,
                                          dt.year,
                                          dic[datetime.datetime.weekday(dt)])
            lista_textos.append(texto)
        lista_textos.reverse()
        for i in lista_textos:
            self.ids.scroll_antigos.add_widget(antigos(text = i,
                                                       size_hint_y = None,
                                                       height = 30))
        self.lista_textos = lista_textos
        
    def data(self):
        dic = {0:'Segunda',1:'Terça',2:'Quarta',3:'Quinta',
               4:'Sexta',5:'Sábado',6:'Domingo'}
        now = datetime.datetime.now()
        if len(str(now.minute)) == 1:
            minuto = '0%s'%now.minute
        else:
            minuto = now.minute
        if len(str(now.hour)) == 1:
            hora = '0%s'%now.hour
        else:
            hora = now.hour
        ds = datetime.datetime.weekday(now)
        dat = '%s - %s/%s/%s - %s:%s'%(dic[ds]
                                       ,now.day,now.month,now.year,hora,minuto)
        return dat

    def local_aplicacao_func(self):
        
        l = [i for i in self.ids.scroll_proximos.children]
        for i in l:
            self.ids.scroll_proximos.remove_widget(i)

        if 'adiantados' not in self.__dict__:

            arq = open('adiantados')
            l = arq.readlines()
            arq.close()
            if len(l) == 0:
                self.adiantados = []
            else:
                self.adiantados = [eval(i) for i in l]

            
            for i in self.adiantados:
                prov = int(i[1])
                self.lista.remove(int(i[0]))
                self.lista.insert(self.lista.index(int(i[1])),int(i[0]))
            
            
        arq = open('aplicados')
        aplic = arq.readlines()
        if len(aplic) == 0:
            ultimo = len(self.lista)
            proximo_ = str(self.lista[0])
            self.ids.local_aplicacao_label.text = proximo_
            ind = 0
        else:
            ultimo = int(aplic[-1].split()[0])
        arq.close()
        for i in range(len(self.lista)):
            
            if i in self.adiantados:
                pass
            else:

                ind_ultima = self.lista.index(ultimo)
                if ind_ultima == len(self.lista) - 1:
                    ind = 0
                else:
                    ind = ind_ultima + 1
                proximo = str(self.lista[ind])
                if len(proximo) == 1:
                    proximo = '0%s'%proximo

                if i != 0:
                    self.ids.scroll_proximos.add_widget(proximos(text = proximo,
                                                               size_hint_y = None,
                                                               height = 40,
                                                        on_release = self.mudar_local))
                if i == 0:
                    self.ids.local_aplicacao_label.text = proximo
                    proximo_ = proximo
                ultimo = int(proximo)

        lp = []
        for l in self.adiantados:
            if l[2] == ultimo:
                lp.append(l)
        for i in lp:
            self.adiantados.remove(i)
        if len(lp) != 0:
            arq = open('adiantados','w')
            for i in self.adiantados:
                arq.write(str(i) + '\n')
            arq.close()

        return proximo_
        
    def mudar_local(self,botao):
        provi = [i for i in self.lista]
        if 'local_original' not in self.__dict__:
            self.local_original = int(self.ids.local_aplicacao_label.text)
        if int(botao.text) == self.local_original:
            self.local_aplicacao_func()
            self.adiantado = False
            return
        prov = self.local_original
        self.ids.local_aplicacao_label.text = botao.text
        self.lista.remove(int(botao.text))
        self.lista.insert(self.lista.index(int(prov)),int(botao.text))
        self.local_aplicacao_func()

        self.lista = [i for i in provi]
        self.adiantado = True

    def insere_aplicacao(self):
        if 'recem_adicionado' in self.__dict__ and self.recem_adicionado != None:
            return
        
        dic = {0:'Segunda',1:'Terça',2:'Quarta',3:'Quinta',
               4:'Sexta',5:'Sábado',6:'Domingo'}
        arq = open('aplicados','a')
        local = self.ids.local_aplicacao_label.text
        now = datetime.datetime.now()
                            
        data = '(%s,%s,%s,%s,%s)'%(now.year,now.month,
                                   now.day,now.hour,now.minute)
        string = '%s \t %s\n'%(local,data)
        arq.write(string); arq.close()
        
        texto = '%s - %s/%s/%s - %s'%(local,now.day,now.month,
                                        now.year,
                                        dic[datetime.datetime.weekday(now)])
        
        self.recem_adicionado = antigos(text = texto,size_hint_y = None, height = 30)
        self.recem_adicionado.add_widget(Button(text = 'X',
                                         width = 1,
            on_release = self.remove_aplicacao))

        self.ids.scroll_antigos.add_widget(self.recem_adicionado,
                                index = -1)
        if self.adiantado == True:
            ind = self.lista_original.index(int(self.ids.local_aplicacao_label.text))
            print(ind)
            if ind == len(self.lista_original) - 1:
                proximo = self.lista_original[0]
                print(self.lista_original)
            else:
                proximo = self.lista_original[ind + 1]
            
                
            arq = open('adiantados','a')
            arq.write('(%s,%s,%s)\n'%(int(self.ids.local_aplicacao_label.text),
                                 int(self.local_original),proximo))
            arq.close()

    def remove_aplicacao(self,b):
        '''apenas a ultima'''

        if 'local_original' in self.__dict__ and \
           int(self.recem_adicionado.text.split('-')[0]) != self.local_original:
            arq = open('adiantados')
            s = arq.readlines(); arq.close()
            arq = open('adiantados','w')
            for i in s[:len(s)-1]:
                arq.write(i)
            arq.close()
        
        self.ids.scroll_antigos.remove_widget(self.recem_adicionado)
        self.recem_adicionado = None
        arq = open('aplicados')
        s = arq.readlines(); arq.close()
        arq = open('aplicados','w')
        for i in s[:len(s)-1]:
            arq.write(i)
        arq.close()
        
        

class App(App):
    
    def build(self):
        return box()
 
App().run()


