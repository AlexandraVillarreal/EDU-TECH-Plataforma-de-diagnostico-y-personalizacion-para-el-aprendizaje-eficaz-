import unittest
import sqlite3
from app import app, DB_PATH

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Cliente de pruebas para Flask
        cls.app.testing = True  # Modo prueba

    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Crear usuario de prueba
        self.cursor.execute("INSERT INTO usuarios (email, contraseña, nombre, apellido) VALUES ('mendoza@test.com', '2367', 'Raquel', 'Mendoza')")
        
        self.conn.commit()

    def tearDown(self):
        self.cursor.execute("DELETE FROM usuarios WHERE email = 'mendoza@test.com'")
        self.conn.commit()
        self.conn.close()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Verifica que responde correctamente

    def test_login(self):
        response = self.app.post('/login', data=dict(email='mendoza@test.com', contraseña='2367'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenido a tu espacio en EDU-TECH.', response.data)  
    def test_registro_usuario(self):
        response = self.app.post('/registro', data=dict(
            email='mendoza@test.com',
            contraseña='2367',
            nombre='Raquel',
            apellido='Mendoza',
            ciclo_1=10, ciclo_2=13, ciclo_3=10
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        # Verifica que el usuario se haya guardado en la BD
        self.cursor.execute("SELECT * FROM usuarios WHERE email = 'mendoza@test.com'")
        usuario = self.cursor.fetchone()
        self.assertIsNotNone(usuario)

        # Limpia el usuario de prueba
        self.cursor.execute("DELETE FROM usuarios WHERE email = 'mendoza@test.com'")
        self.conn.commit()

    def test_recomendaciones(self):
        with self.app.session_transaction() as sess:
            sess['usuario_id'] = 1  # Simula un usuario logueado

        response = self.app.get('/recomendaciones')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recomendaciones', response.data)

if __name__ == '__main__':
    unittest.main()
