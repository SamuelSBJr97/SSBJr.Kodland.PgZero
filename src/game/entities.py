"""Entidades do jogo: jogador, salas, guardiões, livros, mapa, UI simples.

Estas implementações são leves — focadas em estrutura e testabilidade —
e não assumem objetos gráficos concretos (mantêm dados e hooks draw/update).
"""
from typing import List, Optional, Dict, Any
from .base import GameObject


class Livro(GameObject):
    def __init__(self, id: str, title: str, x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.id = id
        self.title = title
        self.collected = False

    def collect(self) -> None:
        self.collected = True


class Guardiao(GameObject):
    def __init__(self, name: str, x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.name = name
        self.dialogue: List[str] = []

    def speak(self) -> Optional[str]:
        return self.dialogue[0] if self.dialogue else None


class Sala(GameObject):
    def __init__(self, name: str, description: str = "", x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.name = name
        self.description = description
        self.items: List[GameObject] = []
        self.guardians: List[Guardiao] = []

    def add_item(self, item: GameObject) -> None:
        self.items.append(item)

    def add_guardian(self, g: Guardiao) -> None:
        self.guardians.append(g)


class Jogador(GameObject):
    def __init__(self, name: str = "Player", x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.name = name
        self.inventory: Dict[str, Livro] = {}
        self.health: int = 100

    def pick_book(self, book: Livro) -> None:
        if book and not book.collected:
            book.collect()
            self.inventory[book.id] = book

    def has_book(self, book_id: str) -> bool:
        return book_id in self.inventory


class Mapa:
    """Representação simples de mapa com salas conectadas."""

    def __init__(self):
        self.rooms: Dict[str, Sala] = {}
        self.connections: Dict[str, List[str]] = {}

    def add_room(self, room: Sala) -> None:
        self.rooms[room.name] = room

    def connect(self, a: str, b: str) -> None:
        self.connections.setdefault(a, []).append(b)
        self.connections.setdefault(b, []).append(a)


class Cidade(Mapa):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class Estrada(Mapa):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class UILivro:
    """UI para exibir informação de um livro."""

    def __init__(self, livro: Livro):
        self.livro = livro

    def render(self, surface: Any) -> None:
        # placeholder; no drawing code to keep testability
        pass


class UIQuestionario:
    """UI que apresenta perguntas (quiz) associadas a um livro/guardian."""

    def __init__(self, questions: Optional[List[Dict[str, Any]]] = None):
        self.questions = questions or []
        self.current = 0

    def answer(self, idx: int) -> bool:
        # Retorna True se acertou — placeholder simples
        q = self.questions[self.current]
        correct = q.get("answer")
        self.current = min(self.current + 1, len(self.questions) - 1)
        return idx == correct


class UIHud:
    """HUD simples que mostra status do jogador."""

    def __init__(self, player: Jogador):
        self.player = player

    def render(self, surface: Any) -> None:
        # Apenas placeholder
        pass
