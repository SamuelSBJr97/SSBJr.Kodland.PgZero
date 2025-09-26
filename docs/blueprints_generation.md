## Geração procedural (Blueprint-like)

Descreve a lógica que constrói conjuntos de componentes (salas convexas de 35
células) e as conecta por estradas com até 3 nós entre componentes.

```mermaid
flowchart TD
  Start([Start Generation]) --> CreateSeed["CreateSeed()\n- random seed (run-id)"]
  CreateSeed --> ForEachComp["for i in range(N=5):\n- GenerateComponent()"]
  ForEachComp --> GenerateComponent["GenerateComponent()\n- build convex shape\n- ensure 35 cells navigable\n- place 3 bugs randomly\n- place door cell(s)"]
  GenerateComponent --> PlaceInGraph["PlaceInGraph()\n- pick graph node / coords"]
  PlaceInGraph --> ConnectGraph["ConnectGraph()\n- connect to existing nodes\n- ensure path length <=3 between components"]
  ConnectGraph --> EvaluateLayout["EvaluateLayout()\n- collision checks\n- pathfinding viability"]
  EvaluateLayout -->|ok| Commit["Commit component to map"]
  EvaluateLayout -->|bad| Regenerate["Regenerate component shape / position"]
  Commit --> ContinueLoop
  ContinueLoop --> EndGeneration["After all components placed:\n- finalize roads\n- compute travel routes"]
  EndGeneration --> Done([Generation Done])

  style Done fill:#dfd,stroke:#333,stroke-width:1px

```

Observações:
- A geração prioriza conectividade e restrições de distância (até 3 nós).
- Componentes devem ser convexos e ter exatamente 35 células úteis para
  navegação.
