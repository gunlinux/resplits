# Max Payne 3 autosplitter helper 

## Todo

- [x] split structure CHAPTER 1
- [x] split structure CHAPTER 2
- [x] split loader
- [x] split render 
- [ ] split saver
- [ ] subsplits to single splits
- [ ] best run VIEW
- [ ] megasplit to levels
- [ ] levels => megasplit
- [ ] metadata load from bs [afterparty]
- [ ] how to io.split will parse single level with random ID
- [ ] split.io stats be like https://splits.io/b0if


## Split structure

```
<?xml version="1.0" encoding="UTF-8"?>
<Run version="1.7.0">
  <GameIcon />
  <GameName>Max Payne 3</GameName>
  <CategoryName>Arcade Mode</CategoryName>
  <LayoutPath>
  </LayoutPath>
  <Metadata>
    <Run id="" />
    <Platform usesEmulator="False">PC</Platform>
    <Region>
    </Region>
    <Variables>
      <Variable name="Misc. Difficulty Subcat">NYM HC, Any%</Variable>
    </Variables>
  </Metadata>
  <Offset>00:00:00</Offset>
  <AttemptCount>337</AttemptCount>
  <AttemptHistory>
    <Attempt id="1" started="08/11/2023 06:20:43" isStartedSynced="False" ended="08/11/2023 06:21:06" isEndedSynced="False" />
    <Attempt id="2" started="08/11/2023 06:21:06" isStartedSynced="False" ended="08/11/2023 06:21:10" isEndedSynced="False" />
    ...
    <Attempt id="65" started="08/16/2023 03:35:07" isStartedSynced="False" ended="08/16/2023 04:56:29" isEndedSynced="False">
      <RealTime>01:21:22.2526321</RealTime>
      <GameTime>00:39:55.3530000</GameTime>
    </Attempt>
    ...
  </attempthistory>
  <segments>
    <segment>
      <name>-c1_0</name>
      <icon />
      <splittimes>
        <splittime name="personal best" />
      </splittimes>
      <bestsegmenttime>
        <realtime>00:00:04.0285476</realtime>
        <gametime>00:00:00.0030000</gametime>
      </bestsegmenttime>
      <segmenthistory>
        <time id="1">
          <realtime>00:00:09.0381007</realtime>
          <gametime>00:00:00.0170000</gametime>
        </time>                        
        ...
        </SegmentHistory>
    </Segment>  
    ...
  </Segments>
  <AutoSplitterSettings />
</Run>

### AFTERPARTY
        "MetaData": {
            "run_id": None,
            "Platform": {userEmulator: False, value: "PC"},
            "Region": ""
                      "Variables": {name: "", "value": NYM HC, ANY %}
    }
