from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status

class AuthenticationUserTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('programas-list') #pega do arquivo urls.py o basename programas e o -list pega para fazer requisicao GET
        self.user = User.objects.create_user('c3po', password='123456')

    def test_autenticacao_user_com_credenciais_corretas(self):
        """Teste que verificar a autenticação de um user com as credenciais corretas"""
        user = authenticate(username='c3po', password='123456')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_requisicao_get_nao_autorizada(self):
        """Verifica uma requisição GET não autorizada"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_autenticacao_user_incorreto(self):
        """Teste que verificar autenticacao de username correto"""
        user = authenticate(username='c3px', password='123456')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_autenticacao_pass_incorreto(self):
        """Teste que verificar autenticacao de password correto"""
        user = authenticate(username='c3po', password='123453')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_requisicao_get_com_user_autenticado(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)