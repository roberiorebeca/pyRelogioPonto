# -*- coding: utf-8 -*-
import unittest

from _warnings import warn
from relogioponto.base import RelogioPonto, Colaborador
import time
from threading import Thread
import os

RELOGIO_ENDERECO = '10.3.0.10'
CALLBACK_OK = False

class TestColaborador(unittest.TestCase):
    
    def setUp(self):
        self.endereco = RELOGIO_ENDERECO
        self.relogio = RelogioPonto(self.endereco)
        self.relogio.conectar() 
        self.colaborador = Colaborador(self.relogio)
        
    def tearDown(self):
        self.relogio.desconectar()
        del self.relogio   
         
    def test_colaborador(self):        
        self.assertEqual(self.colaborador.relogio, self.relogio)
    
    def test_salvar(self):
        if type(self.relogio) == RelogioPonto:
            with self.assertRaises(NotImplementedError) as e:
                self.colaborador.save()
        else:            
            self.colaborador.save()
    
    

class TestRelogioPonto(unittest.TestCase):

    def setUp(self):
        self.endereco = RELOGIO_ENDERECO
        self.totalcolaboradors = 0
        self.relogio = RelogioPonto(self.endereco)
        self.relogio.conectar() 
        self.callback_ok = False
        
    def tearDown(self):
        self.relogio.desconectar()
        del self.relogio 
   

    def test_conexao(self):
        self.assertTrue(self.relogio.conectado, u'Não conectado. Verifique o endereco se está correto ou se o dispositivo está conectado.')

        
    def test_listarcolaboradors(self):      
        with self.assertRaises(NotImplementedError) as e:
            lista = self.relogio.colaboradores
    
    def test_gravarcolaborador(self):
        colaborador = None       
        with self.assertRaises(NotImplementedError) as e:
            lista = self.relogio.gravar_colaborador(colaborador)
            
    def test_apagarcolaborador(self):
        colaborador = None       
        with self.assertRaises(NotImplementedError) as e:
            lista = self.relogio.apagar_colaborador(colaborador)
            
    
    def test_enviarcomando(self):
        try:
            os.remove('callback_ok')
        except:
            pass
        def run():
            self.relogio.add_listener(self.callback_enviarcomando)
            self.relogio.enviar_comando(chr(0))
        Thread(target=run).start()
        time.sleep(0.5)
        self.assertTrue(os.path.isfile('callback_ok'))     
        
        
    def callback_enviarcomando(self, data):
        fo = open("callback_ok", "wb")
        fo.write('ok')
        fo.close()

            
if __name__ == '__main__':
    unittest.main()
    
    