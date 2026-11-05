import pytest
import os
import sys
import uuid

# Adiciona a pasta principal do projeto ao caminho de importação
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_criar_usuario():
    usuario_teste = {
        "nome": "Usuário Teste",
        "email": f"teste_{uuid.uuid4().hex}@example.com",
        "senha": "password"
    }

    resposta = client.post(
        "/auth/criar_conta",
        json=usuario_teste
    )

    assert resposta.status_code == 200

def test_criar_usuario_email_duplicado():
    usuario_teste = {
        "nome": "Usuário Teste",
        "email": f"duplicado_{uuid.uuid4().hex}@example.com",
        "senha": "password"
    }

    primeira_resposta = client.post(
        "/auth/criar_conta",
        json=usuario_teste
    )

    assert primeira_resposta.status_code == 200

    segunda_resposta = client.post(
        "/auth/criar_conta",
        json=usuario_teste
    )

    assert segunda_resposta.status_code == 400

    assert segunda_resposta.json()["detail"] == (
        "E-mail do usuário já cadastrado"
    )