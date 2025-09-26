````markdown
## Geração procedural de salas (forma convexa de 35 células) e IA de bugs

Diagrama que descreve a pipeline de geração procedural de salas com piso
composto por 35 células em formato convexo, caminhos procedurais conectando
o jogador às salas, regras de movimento (jogador só anda sobre células vazias),
porta posicionada no canto da sala e geração ocorrendo 3 blocos adiante da
área do jogador. Inclui também um diagrama de máquina de estados para a IA dos
bugs (cerco + ataque).

```mermaid
%% Pipeline de geração procedural — visão geral
graph TD
  Start([Player moves / world tick]) --> CheckAhead{Player area + lookahead}
  CheckAhead -->|if distance >= chunk_size| GenerateAhead["Gerar chunks 3 blocos à frente"]
  GenerateAhead --> ForEachRoom["Para cada sala a gerar"]

  subgraph RoomGeneration [Geração da sala]
    direction TB
    ForEachRoom --> GenShape["Gerar forma convexa\n35 células (tile-based)"]
    GenShape --> EnsureDoor["Garantir porta no canto\n(posição de canto válida)"]
    EnsureDoor --> CarveFloors["Marcar 35 células como chão\n(o resto bloqueado)"]
  end

  CarveFloors --> ConnectPaths["Gerar caminho procedural\n(conectividade: A* / carve walk)"]
  ConnectPaths --> SpawnBugs["Posicionar bugs nas bordas e entradas\n(instrumentar IA de cerco)"]
  SpawnBugs --> ValidateCells["Marcar células ocupadas: itens/bugs/portas\n(jogador só pode andar sobre vazias)"]
  ValidateCells --> RoomReady([Sala pronta])
  RoomReady --> Integrate["Integrar no mapa e atualizar conexões"]
  Integrate --> End([Ready to be entered])

  %% notas e regras
  classDef note fill:#f9f,stroke:#333,stroke-width:1px
  Rules["Regras importantes:\n- Sala: exatamente 35 células de chão (convexo)\n- Porta: posição obrigatória em um canto da sala\n- Movimentação: jogador só sobre células vazias\n- Geração lookahead: 3 blocos adiante do jogador\n- Caminhos: gerados proceduralmente garantindo conectividade"]:::note
  Rules -.-> GenerateAhead
  Rules -.-> GenShape

  style GenShape fill:#e3f2fd,stroke:#0288d1
  style SpawnBugs fill:#fff3e0,stroke:#fb8c00

``` 

```mermaid
%% Máquina de estados (IA dos bugs): cerco e ataque
stateDiagram-v2
  [*] --> Patrol
  Patrol --> Alerted : detect player (sound/vision)
  Alerted --> Surrounding : evaluate flank points
  Surrounding --> Approaching : move to surround positions
  Approaching --> Attacking : in attack range
  Attacking --> Retreating : low hp or heavy damage
  Retreating --> Patrol : lost interest / regroup
  Attacking --> Dead : hp <= 0
  Patrol --> Sleeping : out of active area
  Sleeping --> Patrol : reactivated

  %% Transições táticas
  note right of Surrounding
    - Ordem: múltiplos bugs calculam posições de cerco
    - Objetivo: forçar jogador a recuar para entradas/porta
  end note

  note right of Approaching
    - Uso de caminhos procedurais pre-calculados (path nodes)
    - Respeitar células bloqueadas (não atravessar paredes)
  end note

```

Breve explicação
- A pipeline gera chunks (blocos) adiante do jogador (lookahead = 3) e monta
  salas com 35 células em formato convexo — isso garante salas de tamanho
  controlado e previsível, porém com variação de forma.
- Cada sala tem uma porta posicionada em um dos cantos; os caminhos são
  esculpidos proceduralmente para conectar o jogador à porta/entrada.
- Bugs têm uma máquina de estados que prioriza cerco (surround) e depois ataque;
  movimento e IA respeitam o mapa de células para evitar atravessar paredes.

````
