"""Classes base leves para objetos e jogo.

Estas classes são pensadas para serem fáceis de testar sem depender do loop
de pgzero. Elas expõem métodos hook que podem ser usados por um wrapper
de integração com pgzero se necessário.
"""
from typing import Tuple, Optional, List, Dict, Any, Callable
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class GameObject:
    """Objeto de jogo básico.

    Responsabilidades:
    - manter posição (x, y)
    - manter visibilidade e ativo/inativo
    - fornecer hooks update(dt) e draw(surface)
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0, height: float = 0):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.visible = True
        self.active = True

    @property
    def pos(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def set_pos(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def update(self, dt: float) -> None:
        """Atualiza o estado do objeto. dt é o delta time em segundos."""
        pass

    def compute_next_state(self, dt: float) -> Optional[Dict[str, Any]]:
        """Opcional: calcular o próximo estado sem mutar o objeto.

        Deve retornar uma estrutura imutável (por exemplo, dict) que represente
        as mudanças a aplicar. O método padrão retorna None.
        """
        return None

    def apply_state(self, state: Optional[Dict[str, Any]]) -> None:
        """Aplica o estado retornado por compute_next_state na thread principal.

        Implementação genérica atualiza a posição quando o campo 'pos' é fornecido.
        Sobrescreva quando necessário.
        """
        if not state:
            return
        pos = state.get('pos')
        if pos is not None:
            try:
                x, y = pos
                self.set_pos(x, y)
            except Exception:
                # ignore malformed state
                pass

    def draw(self, surface) -> None:
        """Desenha o objeto na surface (modo pgzero/pygame)."""
        pass

    def compute_draw(self, surface) -> Optional[Any]:
        """Opcional: preparar dados de desenho fora da thread principal.

        Deve retornar uma estrutura que será passada para apply_draw. Por
        padrão retorna None, o que indica que a implementação tradicional
        de draw deve ser chamada na thread principal.
        """
        return None

    def apply_draw(self, surface, render_data: Optional[Any]) -> None:
        """Aplica o render_data na surface na thread principal.

        Por padrão, se render_data for None, chama o método draw clássico.
        Sobrescreva para aplicar buffers ou dados retornados por compute_draw.
        """
        if render_data is None:
            # fallback para compatibilidade
            self.draw(surface)
        else:
            # implementação genérica não sabe compor render_data; subclasses
            # devem sobrescrever apply_draw se retornam render_data em compute_draw
            self.draw(surface)


class BaseGame:
    """Gerenciador simples de jogo.

    Mantém uma lista de GameObject, provê update/draw e utilitários.
    Projetado para ser usado tanto em testes quanto integrado ao pgzero.
    """

    def __init__(self):
        self.objects: List[GameObject] = []
        self.width: Optional[int] = None
        self.height: Optional[int] = None

    def add(self, obj: GameObject) -> None:
        self.objects.append(obj)

    def remove(self, obj: GameObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self, dt: float) -> None:
        """Chama update em todos objetos ativos usando paralelismo obrigatório.

        Objetos que sobrescreveram compute_next_state serão processados em um
        pool de threads, e seus estados retornados serão aplicados com
        apply_state na thread principal. Objetos que não implementarem
        compute_next_state executarão update(dt) sequencialmente.
        """
        objs = list(self.objects)

        # separar objetos que implementam compute_next_state (sobrescrito)
        parallel_objs: List[GameObject] = []
        serial_objs: List[GameObject] = []
        for obj in objs:
            if not obj.active:
                continue
            # detecta se a classe sobrescreveu compute_next_state
            if obj.__class__.compute_next_state is not GameObject.compute_next_state:
                parallel_objs.append(obj)
            else:
                serial_objs.append(obj)

        # executar compute_next_state em threads e aplicar resultados
        if parallel_objs:
            max_workers = min(32, (os.cpu_count() or 1) * 2)
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                futures = {ex.submit(o.compute_next_state, dt): o for o in parallel_objs}
                for fut in as_completed(futures):
                    o = futures[fut]
                    try:
                        state = fut.result()
                    except Exception:
                        state = None
                    try:
                        o.apply_state(state)
                    except Exception:
                        # aplicar falha não deve quebrar o loop principal
                        pass

        # executar updates seriais (aqueles que não possuem compute_next_state)
        for o in serial_objs:
            try:
                o.update(dt)
            except Exception:
                # garantir que uma falha em um objeto não pare o loop
                pass

    def draw(self, surface) -> None:
        """Chama draw em todos objetos visíveis.

        Se parallel=True, objetos que sobrescreveram compute_draw terão essa
        função executada em um pool de threads; seus resultados são então
        aplicados com apply_draw na thread principal respeitando a ordem de
        composição (ordem em self.objects).
        """
        # compat: old signature draw(surface) -> assumes parallel True
        return self.draw_parallel(surface)

    def draw_parallel(self, surface, parallel: bool = True) -> None:
        objs = list(self.objects)
        if not parallel:
            for obj in objs:
                if obj.visible:
                    obj.draw(surface)
            return

        # separar objetos que implementam compute_draw
        parallel_objs: List[GameObject] = []
        for obj in objs:
            if obj.visible and obj.__class__.compute_draw is not GameObject.compute_draw:
                parallel_objs.append(obj)

        render_results: Dict[GameObject, Any] = {}
        if parallel_objs:
            max_workers = min(32, (os.cpu_count() or 1) * 2)
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                futures = {ex.submit(o.compute_draw, surface): o for o in parallel_objs}
                for fut in as_completed(futures):
                    o = futures[fut]
                    try:
                        render_results[o] = fut.result()
                    except Exception:
                        render_results[o] = None

        # aplicar em ordem para preservar layering
        for obj in objs:
            if not obj.visible:
                continue
            if obj in render_results:
                try:
                    obj.apply_draw(surface, render_results[obj])
                except Exception:
                    # fallback para desenho tradicional
                    try:
                        obj.draw(surface)
                    except Exception:
                        pass
            else:
                try:
                    obj.draw(surface)
                except Exception:
                    pass

    def run(self, fps: int, surface_provider: Optional[Callable[[], object]] = None, frames: Optional[int] = None, stop_event: Optional[threading.Event] = None) -> None:
        """Loop de execução que respeita a taxa de frames definida.

        Args:
            fps: frames por segundo desejados (taxa fixa).
            surface_provider: callable que retorna a surface a cada frame (opcional).
            frames: número máximo de frames a executar (None = infinito até stop_event).
            stop_event: opcional threading.Event para encerrar o loop externamente.
        """
        if fps <= 0:
            raise ValueError("fps must be > 0")
        frame_time = 1.0 / float(fps)
        frame_count = 0
        while frames is None or frame_count < frames:
            start = time.perf_counter()
            dt = frame_time

            # update (paralelo)
            try:
                self.update(dt)
            except Exception:
                pass

            # draw (paralelo)
            surface = None
            if surface_provider is not None:
                try:
                    surface = surface_provider()
                except Exception:
                    surface = None
            try:
                self.draw_parallel(surface, parallel=True)
            except Exception:
                pass

            frame_count += 1
            if stop_event is not None and stop_event.is_set():
                break

            elapsed = time.perf_counter() - start
            sleep_for = frame_time - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

    def clear(self) -> None:
        self.objects.clear()
