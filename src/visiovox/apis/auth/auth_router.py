from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from typing import Any
from .user_models import UserCreate, Token, UserProfile, ErrorResponse
from .jwt_handler import create_jwt_token, refresh_jwt_token, blacklist_token
from .oauth2_scheme import get_current_user
from ..i18n import t

def get_auth_router() -> APIRouter:
    """
    Cria e retorna o APIRouter com todos os endpoints de autenticação.
    Assegura integração com i18n e dependências de autenticação.
    """
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post("/login", response_model=Token, responses={401: {"model": ErrorResponse}})
    async def login(data: UserCreate, request: Request) -> Any:
        """
        Autentica usuário e retorna JWT.
        """
        # TODO: Autenticar usuário, gerar e retornar JWT. Usar i18n para mensagens de erro.
        pass

    @router.post("/logout", responses={200: {"description": "Logged out successfully"}})
    async def logout(token: str = Depends(get_current_user), request: Request = None) -> Any:
        """
        Invalida o token JWT atual.
        """
        # TODO: Blacklist token e retornar resposta i18n
        pass

    @router.post("/register", response_model=UserProfile, responses={400: {"model": ErrorResponse}})
    async def register(data: UserCreate, request: Request) -> Any:
        """
        Registra um novo usuário.
        """
        # TODO: Registrar usuário, retornar UserProfile, usar i18n para erros.
        pass

    @router.post("/refresh", response_model=Token, responses={401: {"model": ErrorResponse}})
    async def refresh(token: str = Depends(get_current_user), request: Request = None) -> Any:
        """
        Renova o token JWT, retornando um novo.
        """
        # TODO: Renovar token usando refresh_jwt_token
        pass

    @router.get("/me", response_model=UserProfile, responses={401: {"model": ErrorResponse}})
    async def get_me(current_user: UserProfile = Depends(get_current_user), request: Request = None) -> Any:
        """
        Retorna perfil do usuário autenticado.
        """
        # TODO: Retornar dados do usuário autenticado, com suporte a i18n
        pass

    return router 