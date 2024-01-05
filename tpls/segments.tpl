{% set date_format = '%m/%d/%Y %H:%M:%S' %}
{% for segment in segments %}
  <name>{{segment.name}}</name>
  <icon>{{segment.icon}}</icon>
  <splittimes>
    <splittime name="personal best" />
  </splittimes>
  <bestsegmenttime>
    {% if segment.bestsegmenttime -%}
    <realtime>{{ segment.bestsegmenttime.Realtime }}</realtime>
    <gametime>{{ segment.bestsegmenttime.Gametime }}</gametime>
    {% endif -%}
  </bestsegmenttime>
  <segmenthistory>
    {% for history in segment.segmentshistory -%}
    <time id="{{ history.id }}">
      <realtime>{{ history.Realtime }}</realtime>
      <gametime>{{ history.Gametime }}</gametime>
    </time>
    {% endfor -%}
{% endfor -%}
