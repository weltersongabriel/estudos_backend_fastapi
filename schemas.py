from pydantic import BaseModel
from typing import List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str

    class Config:
        from_attributes = True
        extra = "forbid"

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True

class ResponseItemPedidoSchema(BaseModel):
    id: int
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True

class PedidoDetalheSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ResponseItemPedidoSchema]

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    quantidade_itens_pedido: int
    pedido: PedidoDetalheSchema

    class Config:
        from_attributes = True
