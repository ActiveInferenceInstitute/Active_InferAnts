"""
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
             xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
             xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
             id="ActiveInferAntsSimulation">

  <process id="AntSimulationProcess" isExecutable="false">
    <startEvent id="SimulationStart">
      <outgoing>flow1</outgoing>
    </startEvent>

    <task id="InitializeEnvironment" name="Initialize Simulation Environment">
      <incoming>flow1</incoming>
      <outgoing>flow2</outgoing>
    </task>

    <task id="CreateAnts" name="Create Active InferAnts">
      <incoming>flow2</incoming>
      <outgoing>flow3</outgoing>
    </task>

    <task id="SetSimulationParameters" name="Set Simulation Parameters">
      <incoming>flow3</incoming>
      <outgoing>flow4</outgoing>
    </task>

    <subProcess id="SimulationLoop" name="Simulation Loop">
      <incoming>flow4</incoming>
      <outgoing>flow17</outgoing>

      <startEvent id="LoopStart">
        <outgoing>flow5</outgoing>
      </startEvent>

      <parallelGateway id="AntActions">
        <incoming>flow5</incoming>
        <outgoing>flow6</outgoing>
        <outgoing>flow7</outgoing>
        <outgoing>flow8</outgoing>
        <outgoing>flow9</outgoing>
        <outgoing>flow22</outgoing>
      </parallelGateway>

      <task id="Perceive" name="Ants Perceive Environment">
        <incoming>flow6</incoming>
        <outgoing>flow10</outgoing>
      </task>

      <task id="Act" name="Ants Perform Actions">
        <incoming>flow7</incoming>
        <outgoing>flow11</outgoing>
      </task>

      <task id="UpdateBeliefs" name="Update Ant Beliefs">
        <incoming>flow8</incoming>
        <outgoing>flow12</outgoing>
      </task>

      <task id="InteractWithOtherAnts" name="Interact With Other Ants">
        <incoming>flow9</incoming>
        <outgoing>flow13</outgoing>
      </task>

      <task id="AdaptToEnvironment" name="Adapt to Environment Changes">
        <incoming>flow22</incoming>
        <outgoing>flow23</outgoing>
      </task>

      <parallelGateway id="SyncAntActions">
        <incoming>flow10</incoming>
        <incoming>flow11</incoming>
        <incoming>flow12</incoming>
        <incoming>flow13</incoming>
        <incoming>flow23</incoming>
        <outgoing>flow14</outgoing>
      </parallelGateway>

      <task id="UpdateEnvironment" name="Update Environment">
        <incoming>flow14</incoming>
        <outgoing>flow15</outgoing>
      </task>

      <task id="CollectSimulationData" name="Collect Simulation Data">
        <incoming>flow15</incoming>
        <outgoing>flow16</outgoing>
      </task>

      <exclusiveGateway id="CheckSimulationEnd">
        <incoming>flow16</incoming>
        <outgoing>flow18</outgoing>
        <outgoing>flow19</outgoing>
      </exclusiveGateway>

      <endEvent id="LoopEnd">
        <incoming>flow18</incoming>
      </endEvent>

      <sequenceFlow id="flow5" sourceRef="LoopStart" targetRef="AntActions" />
      <sequenceFlow id="flow6" sourceRef="AntActions" targetRef="Perceive" />
      <sequenceFlow id="flow7" sourceRef="AntActions" targetRef="Act" />
      <sequenceFlow id="flow8" sourceRef="AntActions" targetRef="UpdateBeliefs" />
      <sequenceFlow id="flow9" sourceRef="AntActions" targetRef="InteractWithOtherAnts" />
      <sequenceFlow id="flow22" sourceRef="AntActions" targetRef="AdaptToEnvironment" />
      <sequenceFlow id="flow10" sourceRef="Perceive" targetRef="SyncAntActions" />
      <sequenceFlow id="flow11" sourceRef="Act" targetRef="SyncAntActions" />
      <sequenceFlow id="flow12" sourceRef="UpdateBeliefs" targetRef="SyncAntActions" />
      <sequenceFlow id="flow13" sourceRef="InteractWithOtherAnts" targetRef="SyncAntActions" />
      <sequenceFlow id="flow23" sourceRef="AdaptToEnvironment" targetRef="SyncAntActions" />
      <sequenceFlow id="flow14" sourceRef="SyncAntActions" targetRef="UpdateEnvironment" />
      <sequenceFlow id="flow15" sourceRef="UpdateEnvironment" targetRef="CollectSimulationData" />
      <sequenceFlow id="flow16" sourceRef="CollectSimulationData" targetRef="CheckSimulationEnd" />
      <sequenceFlow id="flow18" name="Simulation Complete" sourceRef="CheckSimulationEnd" targetRef="LoopEnd" />
      <sequenceFlow id="flow19" name="Continue Simulation" sourceRef="CheckSimulationEnd" targetRef="LoopStart" />
    </subProcess>

    <task id="AnalyzeResults" name="Analyze Simulation Results">
      <incoming>flow17</incoming>
      <outgoing>flow20</outgoing>
    </task>

    <task id="GenerateVisualization" name="Generate Visualization">
      <incoming>flow20</incoming>
      <outgoing>flow21</outgoing>
    </task>

    <task id="ExportData" name="Export Simulation Data">
      <incoming>flow21</incoming>
      <outgoing>flow24</outgoing>
    </task>

    <endEvent id="SimulationEnd">
      <incoming>flow24</incoming>
    </endEvent>

    <sequenceFlow id="flow1" sourceRef="SimulationStart" targetRef="InitializeEnvironment" />
    <sequenceFlow id="flow2" sourceRef="InitializeEnvironment" targetRef="CreateAnts" />
    <sequenceFlow id="flow3" sourceRef="CreateAnts" targetRef="SetSimulationParameters" />
    <sequenceFlow id="flow4" sourceRef="SetSimulationParameters" targetRef="SimulationLoop" />
    <sequenceFlow id="flow17" sourceRef="SimulationLoop" targetRef="AnalyzeResults" />
    <sequenceFlow id="flow20" sourceRef="AnalyzeResults" targetRef="GenerateVisualization" />
    <sequenceFlow id="flow21" sourceRef="GenerateVisualization" targetRef="ExportData" />
    <sequenceFlow id="flow24" sourceRef="ExportData" targetRef="SimulationEnd" />
  </process>

  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="AntSimulationProcess">
      <!-- BPMN diagram elements -->
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</definitions>
"""
