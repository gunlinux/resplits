{% set date_format = '%m/%d/%Y %H:%M:%S' %}
{% for attempt in attempts %}
    <Attempt id="{{attempt.id}}" started="{{attempt.started.strftime(date_format)}}" isStartedSynced="attempt.isStartedSynced" ended="{{attempt.ended.strftime(date_format)}}" isEndedSynced="{{attempt.isEndedSynced}}">
      {% if attempt.runtime -%}
          <RealTime>{{attempt.runtime.Realtime}}</RealTime>
          <GameTime>{{attempt.runtime.Gametime}}</GameTime>
      {% endif -%}</Attempt>
{% endfor %}