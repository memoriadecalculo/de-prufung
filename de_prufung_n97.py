#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 13/01/2012

@author: Lauro Cavalcanti de Sá
'''
import appuifw, e32, random, graphics
import sys, time

UI_L = u"c:\\Data\\python\\landscape.png"
UI_P = u"c:\\Data\\python\\portrait.png"

class GUI:
    "Interface com usuário."
    def __init__(self):

        # Título:
        appuifw.app.title = u"Artikels Prüfung"

        # Cria o menu com suas funcoes de retorno
        appuifw.app.menu = [(u"Iniciar", self.artigos_teste), (u"Config.", self.fParam_show)]

        # Definindo o tamanho do aplicativo
        appuifw.app.screen = "normal"

        # Define o método a ser chamado quando a tecla direita é pressionada
        appuifw.app.exit_key_handler = self.sair

        # Cria um objeto do serviço de sincronia
        self.app_lock = e32.Ao_lock()

        # Salva informações básicas padrões deste SW:
        self.qt_artigos = 5

        # Define o corpo do aplicativo:
        self.tabs_criar()

    def tabs_criar(self):
        "Cria as páginas do SW."
        self.img = graphics.Image.open(UI_L)
        self.canvas = appuifw.Canvas(redraw_callback = self.img_redraw)

        self.tab2 = appuifw.Text(u"Esta é a Tab2")

        appuifw.app.set_tabs([u"Um", u"Dois"], self.tab_handler)

        appuifw.app.body = self.canvas

        return self.canvas

    def tab_handler(self, index):
        "Troca o corpo do SW de acordo com a página."
        if(index==0):
            appuifw.app.body = self.canvas
        if(index==1):
            appuifw.app.body = self.tab2

    def img_redraw(self, rect):
        "Redesenha a imagem quando solicitado."
        if self.img:
            self.canvas.blit(self.img)

    def fParam_show(self):
        "Exibe o formulário de configurações do programa."

        # Campos para o formulário:
        campos = [(u"Qt. de palavras",'number', self.qt_artigos),]

        #Create a Form object
        fParam = appuifw.Form(campos, flags=appuifw.FFormEditModeOnly)
        #Assign the save function
        fParam.save_hook = self.fParam_salvar
        #Executa o formulário e retorna 'None':
        fParam.execute()

    def fParam_salvar(self, arg):
        "Salva as informações do formulário."
        self.tab2.add(arg[0][2])
        self.qt_artigos = int(arg[0][2])
        return True

    def artigos_teste(self):
        "Executa o teste de artigos."
        # Tipos de artigo:
        artigos = [u"der",u"die",u"das",u"kein"]

        # Carrega lista de palavras a serem testadas
        palavras = {}
        palavras[u"Apfel"] = (0, (u"-el",), (u"Fruchte",))
        palavras[u"Banane"] = (1, (u"Fruchte",), ())
        palavras[u"Auto"] = (2, (u"-o",), ())
        palavras[u"Käse"] = (0, (u"Käse",), (u"-e",))
        palavras[u"Deutschland"] = (0, (u"Länder",), ())

        i = 1
        while i <= self.qt_artigos:
#            n_palavra =
#            t.add(unicode(n_palavra))
#            t.add(palavras.keys()[n_palavra])
            palavra = palavras.keys()[random.randint(0,len(palavras)-1)]
            self.tab2.add(palavra)
            resp = appuifw.popup_menu(artigos, u"___ " + palavra)
            if resp == None:
                break
            i += 1

    def sair(self):
        "Finaliza o SW."
        appuifw.app.set_tabs([], None)
        self.app_lock.signal()
#        appuifw.app.set_exit()

def main():
    app = GUI()
    app.app_lock.wait()

if __name__ == "__main__":
    sys.exit(main())
