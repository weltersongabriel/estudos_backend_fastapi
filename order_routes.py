from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido


order_router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
    dependencies=[Depends(verificar_token)]
)


# ROTA PADRÃO
@order_router.get("/")
async def pedidos():
    """
    Rota padrão de pedidos.
    Todas as rotas precisam de autenticação.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}


# CRIAR PEDIDO
@order_router.post("/pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)

    # Verifica se o usuário está criando o próprio pedido
    if not usuario.admin and usuario.id != pedido_schema.id_usuario:
        raise HTTPException(
            status_code=403,
            detail="Você não tem autorização para criar pedido para outro usuário"
        )

    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)

    return {
        "mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"
    }


# CANCELAR PEDIDO
@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    pedido = session.query(Pedido).filter(
        Pedido.id == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403,
            detail="Você não tem autorização para fazer essa modificação"
        )

    pedido.status = "CANCELADO"

    session.commit()
    session.refresh(pedido)

    return {
        "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }


# LISTAR TODOS OS PEDIDOS (SOMENTE ADMIN)
@order_router.get("/listar")
async def listar_todos_pedidos(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    if not usuario.admin:
        raise HTTPException(
            status_code=403,
            detail="Você não tem autorização para fazer essa operação"
        )

    pedidos = session.query(Pedido).all()

    return {
        "pedidos": pedidos
    }


# ADICIONAR ITEM AO PEDIDO
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(
    id_pedido: int,
    item_pedido_schema: ItemPedidoSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    pedido = session.query(Pedido).filter(
        Pedido.id == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não existente"
        )

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403,
            detail="Você não tem autorização para fazer essa operação"
        )

    item_pedido = ItemPedido(
        item_pedido_schema.quantidade,
        item_pedido_schema.sabor,
        item_pedido_schema.tamanho,
        item_pedido_schema.preco_unitario,
        id_pedido
    )

    session.add(item_pedido)
    session.flush()

    pedido.calcular_preco()

    session.commit()
    session.refresh(pedido)
    session.refresh(item_pedido)

    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }


# REMOVER ITEM DO PEDIDO
@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(
    id_item_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    item_pedido = session.query(ItemPedido).filter(
        ItemPedido.id == id_item_pedido
    ).first()

    if not item_pedido:
        raise HTTPException(
            status_code=404,
            detail="Item no pedido não existente"
        )

    pedido = session.query(Pedido).filter(
        Pedido.id == item_pedido.pedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403,
            detail="Você não tem autorização para fazer essa operação"
        )

    session.delete(item_pedido)
    session.flush()

    pedido.calcular_preco()

    session.commit()
    session.refresh(pedido)

    return {
        "mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }


# FINALIZAR PEDIDO
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    pedido = session.query(Pedido).filter(
        Pedido.id == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403,
            detail="Você não tem autorização para fazer essa modificação"
        )

    pedido.status = "FINALIZADO"

    session.commit()
    session.refresh(pedido)

    return {
        "mensagem": f"Pedido número: {pedido.id} finalizado com sucesso",
        "pedido": pedido
    }


# VISUALIZAR UM PEDIDO ESPECÍFICO
@order_router.get(
    "/pedido/{id_pedido}",
    response_model=ResponsePedidoSchema
)
async def visualizar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    pedido = session.query(Pedido).filter(
        Pedido.id == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403,
            detail="Você não tem autorização para visualizar esse pedido"
        )

    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }


# LISTAR PEDIDOS DO USUÁRIO LOGADO
@order_router.get(
    "/listar/pedidos-usuario",
    response_model=List[ResponsePedidoSchema]
)
async def listar_pedidos_usuario(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    pedidos = session.query(Pedido).filter(
        Pedido.usuario == usuario.id
    ).all()

    return [
        {
            "quantidade_itens_pedido": len(pedido.itens),
            "pedido": pedido
        }
        for pedido in pedidos
    ]
