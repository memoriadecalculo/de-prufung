#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# main.py
# Copyright (C) Lauro Cavalcanti de Sa 2012 <lauro@lcsa>
#
#DE_Prufung is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DE_Prufung is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys

import sys
sys.path.append("../libX/py")

#import gtk
#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "de_prufung_pal_add.glade"
#UI_FILE = "/usr/local/share/de_prufung/ui/de_prufung.ui"

class GUI:
    def __init__(self):

        self.glade_load()
        self.glade_obj_load(self.builder)
        self.generos_load(self.lstGeneros)
        self.palavras_load()
        self.glade_obj_add(self.generos, self.builder)
        self.regras_load(self.lstRegras)
        self.window.show_all()

    def glade_load(self):
        """
        Carrega arquivo 'Glade' com GUI para o objeto 'builder'.
        """
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        return self.builder

    def glade_obj_load(self, builder):
        """
        Carrega objetos a partir do objeto 'builder'.
        Método 'GladeLoad' deve ser chamado antes deste.
        """

        # Grupo de objetos da parte 'adicionar palavras'
        self.etxtPalavra    = builder.get_object("etxtPalavra")
        self.cmbGeneros     = builder.get_object("cmbGeneros")
        self.lstGeneros     = builder.get_object("lstGeneros")
#        self.cmbPalavrasRegras   = builder.get_object("cmbPalavrasRegras")
#        self.cmbPalavrasExcecoes = builder.get_object("cmbPalavrasExcecoes")

        # Grupo de objetos da parte 'apagar palavras'
#        self.cmbPalavrasPalavra = builder.get_object("cmbPalavrasPalavra")
#        self.lPalavrasGenero    = builder.get_object("lPalavrasGenero")
#        self.lPalavrasRegras    = builder.get_object("lPalavrasRegras")
#        self.lPalavrasExcecoes  = builder.get_object("lPalavrasExcecoes")

        # Janela principal:
        self.window = builder.get_object('window')

        # Janela de status e seu ID:
        self.MSG = builder.get_object('stbMSG')
        self.MSGid = self.MSG.get_context_id("mensagens")

        return self.window

    def glade_obj_add(self, generos, builder):
        """
        Adiciona objetos complementares a GUI criada pelo Glade, usando Gtk.
        'generos' representa uma lista com os genêros disponíveis.
        'builder' representa o objeto construtor da GUI.
        """

        # Listas de dados:
        self.lstRegras = []
        self.trvRegras = []
        self.colTxt = []
        self.colTog = []
        self.renTog = []

        renderer_text = Gtk.CellRendererText()

        for iG in range(0, len(generos)):
            self.lstRegras.append(Gtk.ListStore(str, bool))
            self.trvRegras.append(builder.get_object("trvRegras"+str(iG)))
            self.trvRegras[iG].set_model(self.lstRegras[iG])
            self.colTxt.append(Gtk.TreeViewColumn("Text", renderer_text, text=0))
            self.renTog.append(Gtk.CellRendererToggle())
            self.colTog.append(Gtk.TreeViewColumn("Toggle", self.renTog[iG], active=1))
            self.renTog[iG].connect("toggled", self.on_cell_toggled)
            self.trvRegras[iG].append_column(self.colTxt[iG])
            self.trvRegras[iG].append_column(self.colTog[iG])
#            self.colTxt[iG].set_resizable(False)
#            self.colTxt[iG].set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        return self.lstRegras

    def on_cell_toggled(self, widget, path):
        """
        Altera o estado do botão de seleção e salva o novo estado na Lista.
        """
        data = self.trvRegras[self.renTog.index(widget)].get_model()
        data[path][1] = not data[path][1]

    def sair(self, *args):
        import xXML
        xXML.SalvaObjeto(self.palavras, "palavras.xml")
        Gtk.main_quit(*args)

    def palavras_load(self):
        """
        Carrega palavras para um objeto XML na memória.
        """
        import xXML

        # Carregando palavras para objeto XML na memória:
#        from lxml import objectify
#        palavras = xXML.CreateXML("palavras")
        self.palavras = xXML.CarregaObjeto("palavras.xml")

        # Como carregar um GtkComboBoxText com a lista de palavras:
#        i = 0
#        for SubNo in self.palavras.iterchildren():
#            self.cmbPalavrasPalavra.append_text(SubNo.texto.text)
#            i += 1
#        width = 1 + i/20
#        self.cmbPalavrasPalavra.set_wrap_width(width)

        return self.palavras

    def generos_load(self, lstGeneros):
        """
        Carrega lista de gêneros disponíveis.
        'lstGeneros' representa o objeto lista da GUI.
        """
        # Carregando lista de gêneros a partir da GUI:
        self.generos = []
#        self.generos = ['der', 'die', 'das', 'kein Artikel']
        for row in lstGeneros:
            self.generos.append(row[0])

        # Como carregar um GtkComBoxText com os gêneros:
#        for genero in self.generos:
#            self.cmbPalavrasGenero.append_text(genero)
#
        return self.generos

    def regras_load(self, lstRegras):
        """
        Carrega lista de regras disponíveis para as listagens disponíveis no
        objeto 'lstRegras' da GUI.

        """
        import xXML

        self.regras = xXML.CarregaObjeto("regras.xml")

        for regra in self.regras.iterchildren():
            lstRegras[int(regra.genero)].append([regra.texto.text, False])

        return self.regras

    def genero_changed(self, combo):
        """
        Troca as listas entre os TreeViews na GUI a partir do gênero selecionado.
        """

        # Faz a troca de listas entre os objetos TreeView:
        modNovo = self.lstRegras[combo.get_active()]

        for trvRegra in self.trvRegras:
            if trvRegra.get_model() == modNovo:
                trvRegra.set_model(self.trvRegras[0].get_model())
                iVelho = self.trvRegras.index(trvRegra)
                self.trvRegras[0].set_model(modNovo)

        # Redimensiona somente as listas alteradas:
        self.colTxt[0].queue_resize()
        self.colTxt[iVelho].queue_resize()

        # Solicita o redimensionamento de todas as listas:
#        for coluna in self.colTxt:
#            coluna.queue_resize()

    def palavra_add(self, widget):
        """
        Adiciona uma palavra ao objeto XML na memória.
        """

        self.MSG.push(self.MSGid, 'Adicionando nova palavra...')

        from xXML import AddSubNo

        # Pega a palavra e genêro:
        texto = unicode(self.etxtPalavra.get_text(), "utf-8")
        genero = self.cmbGeneros.get_active()

        # Cria um novo nó no objeto XML:
        if texto and genero >= 0:
            SubNo, outMSG = AddSubNo(self.palavras, 'palavra', texto, True)
            if SubNo is not None:
                AddSubNo(SubNo, 'genero', str(genero))
                for iTrv in range(0,len(self.trvRegras)):
                    modelo = self.trvRegras[iTrv].get_model()
                    for linha in modelo:
                        if linha[1]:
                            if iTrv:
                                AddSubNo(SubNo, 'excecao', unicode(linha[0], "utf-8"))
                            else:
                                AddSubNo(SubNo, 'regra', unicode(linha[0], "utf-8"))
                self.MSG.push(self.MSGid, 'Palavra "'+texto+'" adicionada!')
            else:
                self.MSG.push(self.MSGid, outMSG)
            self.palavra_limpeza()
        else:
            self.MSG.push(self.MSGid, 'Palavra ou gênero incorreto(s)!')

    def palavra_limpeza(self):
        """
        Limpa as marcações das listas utilizadas pela palavra anterior.
        """

        for iTrv in self.trvRegras:
            modelo = iTrv.get_model()
            for linha in modelo:
                if linha[1]:
                    linha[1] = not linha[1]

        self.etxtPalavra.set_text("")

        self.cmbGeneros.set_active(-1)
        self.cmbGeneros.grab_focus()

        return self.etxtPalavra

    def palavras_genero(self, combo, data):

        # Ainda não USADO!

        self.MSG.push(self.MSGid, 'Atualizando regras e exceções...aguarde...')

        self.cmbPalavrasRegras.get_model().clear()
        self.cmbPalavrasExcecoes.get_model().clear()

        genero = self.cmbPalavrasGenero.get_active_text()
        if genero != None:
            iR = 0
            iE = 0
            ind = self.generos.index(genero)
            for regra in self.regras.iterchildren():
                if regra.genero == ind:
                    self.cmbPalavrasRegras.append_text(regra.texto.text)
                    iR += 1
                else:
                    self.cmbPalavrasExcecoes.append_text(regra.texto.text)
                    iE += 1
            self.cmbPalavrasRegras.set_wrap_width(1 + iR/15)
            self.cmbPalavrasExcecoes.set_wrap_width(1 + iE/15)

        self.MSG.push(self.MSGid, 'Regras e exceções atualizadas.')

    def palavras_teste(self, combo, data):

        self.MSG.push(self.MSGid, 'Entrou...')
        if combo.has_focus():
            print 'tem foco'
        else:
            print 'sem foco'
        self.MSG.push(self.MSGid, 'Saiu.')

        return True

    def palavras_del(self, widget):
        self.MSG.push(self.MSGid, 'palavras_del.')

def main():
    app = GUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())

# Frequência estimada (%) da validade das regras:
#regeln_oft = ("","manchmal (70%)","fast oft (80%)","oft (90%)","fast immer (99%)","immer (100%)")

# Criação da variável que contém as regras a serem indicadas.
# Formato:
#  chave   = regra
#  1oCampo = tipo do artigo
#  2oCampo = frequência de acordo com regeln_oft
#regeln = {}
#"""
#REGRAS PARA MASCULINO:
#-ant 0 0
#-el 0 0
#-en 0 0
#-ent 0 0
#-er 0 5
#-ig 0 0
#-isch 0 0
#-ismus 0 0
#-ling 0 0
#-or 0 0
#-us 0 4
#Alkohol 0 3
#Automarken 0 3
#Kaffee 0 5
#Käse 0 3
#Monate 0 5
#Substantiv_von_Infinitiv_ohne_-en 0 3
#Tage 0 5
#Tee 0 5
#von_Himmel 0 3
#Währungen 0 3
#1-Silbe 0 1
#
#REGRAS PARA FEMININO:
#-ät 1 0
#-e 1 0
#-ei 1 4
#-enz 1 0
#-heit 1 5
#-ie 1 0
#-ik 1 0
#-in 1 0
#-ion 1 0
#-schaft 1 0
#-thek 1 0
#-tion 1 0
#-tur 1 0
#-ung 1 5
#-[k]t 1 2
#Frucht 1 3
#Zahlen 1 3
#
#REGRAS PARA NEUTRO:
#-al 2 0
#-ar 2 0
#-at 2 3
#-chen 2 5
#-et 2 0
#-ett 2 0
#-ier 2 0
#-ing 2 0
#-ment 2 0
#-o 2 0
#-tel 2 4
#-um 2 0
#-zeug 2 0
#ge- 2 0
#Buchstaben 2 3
#English_Wörter 2 4
#Farben 2 3
#Gramm 2 3
#Metalle 2 3
#Sportarten 2 3
#Telefon 2 3
#Sprachen 2 5
#Substantiv_von_Infinitiv 2 3
#
#REGRAS PARA SEM GÊNERO:
#Länder 3 3
#Namen 3 5
#Städte 3 5
#"""
