## Diagrama de classes (Mermaid)

O diagrama abaixo representa as principais classes implementadas em
`src/game` e `src/game/entities.py`, com heranças e relações principais.

Cole o bloco em um renderizador que suporte Mermaid para visualizar.

```mermaid
classDiagram
    %% Classes base
    class GameObject {
      +float x
      +float y
      +bool visible
      +bool active
      +pos()
      +set_pos(x,y)
      +update(dt)
      +draw(surface)
    }

    class BaseGame {
      +List~GameObject~ objects
      +int? width
      +int? height
      +add(obj)
      +remove(obj)
      +update(dt)
      +draw(surface)
      +clear()
    }

    GameObject <|-- Livro
    GameObject <|-- Guardiao
    GameObject <|-- Sala
    GameObject <|-- Jogador

    BaseGame <|-- Scene
    SceneManager o-- Scene : manages
    Scene ..|> BaseGame

    class Scene {
      +name: str
      +on_enter(prev)
      +on_exit(next)
    }

    class SceneManager {
      -stack: List~Scene~
      +push(scene)
      +pop()
      +replace(scene)
      +current: Scene?
      +update(dt)
      +draw(surface)
    }

    class Game {
      +width
      +height
      +scenes: SceneManager
      +running: bool
      +start(initial_scene?)
      +stop()
      +push_scene(scene)
      +pop_scene()
      +replace_scene(scene)
      +update(dt)
      +draw(surface)
    }

    class Livro {
      +id: str
      +title: str
      +collected: bool
      +collect()
    }

    class Guardiao {
      +name: str
      +dialogue: List~str~
      +speak()
    }

    class Sala {
      +name: str
      +description: str
      +items: List~GameObject~
      +guardians: List~Guardiao~
      +add_item(item)
      +add_guardian(g)
    }

    class Jogador {
      +name: str
      +inventory: Dict~str, Livro~
      +health: int
      +pick_book(book)
      +has_book(id)
    }

    class Mapa {
      +rooms: Dict~str, Sala~
      +connections: Dict~str, List~str~
      +add_room(room)
      +connect(a,b)
    }

    Mapa <|-- Cidade
    Mapa <|-- Estrada

    class Cidade
    class Estrada

    class UILivro
    class UIQuestionario
    class UIHud

    UILivro --> Livro : shows
    UIQuestionario --> QuestionsList : questions
    UIHud --> Jogador : displays status

    class SalasEQuestoes {
      +city: Cidade
      +player: Jogador
      +_build_example()
      +attach_to_game(game)
    }

    SalasEQuestoes --> Mapa : builds
    SalasEQuestoes --> Jogador : creates
    Game --> SceneManager : uses
    SceneManager --> Scene : manages
    Scene --> Sala : contains (semântico)
    Sala "1" o-- "*" Livro : items
    Sala "1" o-- "*" Guardiao : guardians

    %% Nota: classes de 'Bug' e comportamento de combate podem ser
    %% representadas por Guardiao ou por uma nova entidade Enemy/Bug se criada.
```

Breve explicação
- Herança: `GameObject` é pai de entidades que existem na cena (jogador, sala,
  guardiões, livros). `BaseGame` é pai de `Scene`.
- Composição: `Sala` contém `items` (por exemplo `Livro`) e `guardians`.
- `SalasEQuestoes`/`DepuradorProject` monta o `Mapa` e o `Jogador` e injeta no
  `Game` para iniciar a experiência.