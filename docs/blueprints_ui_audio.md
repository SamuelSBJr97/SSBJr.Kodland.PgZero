## UI e Audio (Blueprint-like)

Diagrama resumido mostrando como a UI e o sistema de áudio se conectam ao
gameplay para atualizar HUD e tocar sons.

```mermaid
flowchart TD
  GameLoop([Game Loop]) --> UpdateHUD["Update HUD\n- player.hp\n- bugs_remaining"]
  UpdateHUD --> RenderHUD["Render HUD\n- draw HP bar\n- draw bug counter"]
  GameLoop --> EventSound["Event: sound trigger\n- attack, jump, room cleared"]
  EventSound --> AudioManager["AudioManager.play(sound)"]
  AudioManager --> OutputAudio["Output (music + SFX)"]
  RenderHUD --> Display
  Display -->|user sees UI| Player
  OutputAudio -->|user hears| Player

  subgraph UIComponents
    UILivro["UILivro"]
    UIQuestionario["UIQuestionario"]
    UIHud["UIHud"]
  end

  UIHud --> UpdateHUD
  UILivro --> RenderHUD
  UIQuestionario --> RenderHUD

```

Notas:
- `AudioManager` gerencia canais de música/efeitos e suporta volume/mute.
- UI componentes são leves e recebem estados (player, sala) para renderizar.
