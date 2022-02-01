/*---*/
import "./nodestyles.css";

import React from "react";
import { Handle } from "react-flow-renderer";

const ProcessNode = ({ data }) => {
  return (
    <div className="process-node">
      <Handle type="target" id="top" position="top" />
      <div id={data.id}>{data.label}</div>
      <Handle type="source" id="bottom" position="bottom" />
    </div>
  );
};

const InOutNode = ({ data }) => {
  return (
    <div className="inout-node">
      <span className="tooltiptext">{data.desc}</span>

      <Handle type="target" id="top" position="top" />
      <div id={data.id}>{data.label}</div>
      <Handle type="source" id="bottom" position="bottom" />
    </div>
  );
};

const IFNode = ({ data }) => {
  return (
    <div className="if-node">
      <Handle type="target" id="top" position="top" />
      <div id={data.id}>{data.label}</div>
      <Handle type="source" id="left" position="left"></Handle>
      <div className="elseStyle">else</div>
      <Handle type="source" id="right" position="right" />
      <div className="thenStyle">then</div>
    </div>
  );
};

const EndIFNode = ({ data }) => {
  return (
    <div className="endif-node">
      <Handle type="source" id="bottom" position="bottom" />
      <Handle type="target" id="left" position="left" />
      <Handle type="target" id="right" position="right" />
    </div>
  );
};

export const nodeTypes = {
  process: ProcessNode,
  inout: InOutNode,
  cond: IFNode,
  endif: EndIFNode
};
