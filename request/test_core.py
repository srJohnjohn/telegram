import unittest
from .echobot import texto_da_opcao

class TestCore(unittest.TestCase):
    def test_handle_updates(self):
        self.assertEqual(texto_da_opcao('1'), f'''Queijo quente - R$5,00 Confirmar pedido?(s/n)''')
        self.assertNotEqual(texto_da_opcao('1'), 'babalu')


if __name__ == '__name__':
    unittest.main()