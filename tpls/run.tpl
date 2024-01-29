<?xml version="1.0" encoding="UTF-8"?>
<Run version="1.7.0">
  <GameIcon {% if obj.game_icon %}>{{obj.game_icon}}</GameIcon>{% else %}/>{% endif %}
  <GameName>{{obj.game_name}}</GameName>
  <CategoryName>{{obj.category_name}}</CategoryName>
  <LayoutPath {% if obj.layout_path -%} >{{obj.layout_path}}</LayoutPath>{% else -%} /> {% endif -%} 

  <Metadata>
    <Run id="" />
    <Platform usesEmulator="False">PC</Platform>
    <Region>
    </Region>
    <Variables>
      <Variable name="Misc. Difficulty Subcat">NYM HC, Any%</Variable>
    </Variables>
  </Metadata>
  <Offset>{{obj.offset}}</Offset>
  <AttemptCount>{{obj.attempt_count}}</AttemptCount>
  {{attempt_history}}
  <Segments>{{segments}}</Segments>
  <AutoSplitterSettings />
</Run>
