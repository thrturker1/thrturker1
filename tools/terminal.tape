# Optional Charmbracelet VHS source for maintainers who prefer a shell capture.
# The committed terminal.gif is generated deterministically by generate_terminal.py,
# so VHS is not required in CI.

Output assets/terminal-vhs.gif
Set Shell "bash"
Set FontSize 16
Set Width 1080
Set Height 610
Set Theme { "background": "#02060B", "foreground": "#D8F4FF", "cursor": "#55C8FF" }
Set TypingSpeed 34ms

Type "initialize --identity tahir"
Enter
Sleep 500ms
Type "printf '\\n[OK] identity.core ............... TAHIR\\n[OK] quality_engineering ......... LOADED\\n[OK] creative_engine ............. LOADED\\n[OK] agent_systems ............... LOADED\\n'"
Enter
Sleep 1s
Type "inspect --capabilities"
Enter
Sleep 500ms
Type "printf '\\nQA        :: ISTQB Certified / Full-Stack Quality\\nGAMES     :: Godot / Unity / Blender\\nSOFTWARE  :: .NET / Node.js / Web + Desktop\\nAI        :: Agents / Orchestration / Training\\n'"
Enter
Sleep 1s
Type "launch addictity-games"
Enter
Sleep 500ms
Type "printf '\\n[ONLINE] https://addictitygames.com\\n'"
Enter
Sleep 2s
