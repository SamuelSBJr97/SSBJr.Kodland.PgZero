## Máquinas de estado: Jogador e Bug

Diagrama em Mermaid mostrando estados e transições para o jogador e para os
bugs (inimigos).

```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Moving : input (↑/↓)
  Moving --> Idle : no input
  Idle --> Attacking : press Space
  Attacking --> Idle : attack finished
  Moving --> Attacking : press Space
  Idle --> InRoomExitArea : steps into exit area
  InRoomExitArea --> Idle : steps back
  InRoomExitArea --> Exiting : choose path
  Exiting --> Travel : travel on road
  Travel --> Idle : arrive at component
  Idle --> Damaged : hit by bug
  Damaged --> Idle : recover (invul timer)
  Damaged --> Dead : hp <= 0
  Dead --> Respawn : after penalty
  Respawn --> Idle

  %% Bug state machine (cluster)
  state "Bug" as BUG {
    [*] --> Sleeping
    Sleeping --> Alerted : player leaves door area
    Alerted --> Approaching : decide approach
    Approaching --> Circling : tactical choice
    Approaching --> Jumping : close enough
    Jumping --> Cooldown
    Cooldown --> Alerted
    Circling --> Jumping : attempt pounce
    Alerted --> Dead : hp <=0
    Dead --> [*]
  }

```

Explicação:
- Jogador tem estados básicos de movimento/ataque/dano/respawn.
- Bugs começam dormindo, são alertados quando o jogador sai da área da porta
  e então executam táticas (approach/circle/jump) até morrerem.
