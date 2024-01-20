{% set date_format = '%m/%d/%Y %H:%M:%S' %}
{% for segment in segments %}
<Segment>
  <Name>{{segment.name}}</Name>
  <Icon {% if segment.icon %}>{{segment.icon}}</Icon> {% else %} /> {% endif %}
  <SplitTimes>
    {% for name, runtime in segment.split_times.items() -%}
      <SplitTime name="{{ name }}">
        {% if runtime -%}
        <RealTime>{{ runtime.Realtime }}</RealTime>
        <GameTime>{{ runtime.Gametime }}</GameTime>
        {% endif -%}
      </SplitTime>
    {% endfor -%}
  </SplitTimes>
  <BestSegmentTime>
    {% if segment.bestsegmenttime -%}
    <RealTime>{{ segment.bestsegmenttime.Realtime }}</RealTime>
    <GameTime>{{ segment.bestsegmenttime.Gametime }}</GameTime>
    {% endif -%}
  </BestSegmentTime>

     <SegmentHistory>
    {% for history in segment.segmentshistory -%}
    <Time id="{{ history.id }}">
      <RealTime>{{ history.Realtime }}</RealTime>
      <GameTime>{{ history.Gametime }}</GameTime>
    </Time>
    {% endfor -%}
     </SegmentHistory>
    </Segment>
{% endfor -%}
