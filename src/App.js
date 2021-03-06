import React, { useState, useRef } from "react";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  Controls
} from "react-flow-renderer";
import "./styles.css";
import { nodeTypes } from "./Nodes";

const initialElements = [
  {
    id: "0",
    type: "cond",
    data: { label: "cond1" },
    position: { x: 150, y: 30 }
  },
  {
    id: "1",
    type: "inout",
    data: {
      label: `echo `,
      desc: `### Help for TERAD ###
# Inputs are:
# 1. A file to search for TE in fasta format
# 2. The number of cores to use
# 3. The custom library to search for TE
# 
# Make sure your input file, TERAD, extract_cdhit2.R, and RAD_TE_summary.R in the same folder as well as your custom TE library in fasta format
# 
# Test run:
# ./TERAD test_file.fasta 4 ./arthro_ES_ND_PV_classified.fa none
# or 
# ./TERAD test_file.fasta 4 none arthropods        


# 
# See readme for installation instructions
`
    },
    position: { x: 160, y: 50 }
  },
  {
    id: "2",
    type: "process",
    data: { label: "exit" },
    position: { x: 160, y: 90 }
  },
  { id: "3", type: "endif", position: { x: 160, y: 130 } },
  {
    id: "4",
    type: "inout",
    data: {
      label: `echo `,
      desc: `
########################################
### Thanks for using TERAD
########################################`
    },
    position: { x: 160, y: 150 }
  },
  {
    id: "5",
    type: "inout",
    data: {
      label: `echo `,
      desc: `

########################################
### Input parameters
########################################
`
    },
    position: { x: 160, y: 270 }
  },
  {
    id: "6",
    type: "inout",
    data: { label: `echo `, desc: `"1. File name: $1"` },
    position: { x: 160, y: 310 }
  },
  {
    id: "7",
    type: "inout",
    data: { label: `echo `, desc: `"2. No. of cores: $2"` },
    position: { x: 160, y: 350 }
  },
  {
    id: "8",
    type: "inout",
    data: { label: `echo `, desc: `"3. Path to TE database: $3"` },
    position: { x: 160, y: 390 }
  },
  {
    id: "9",
    type: "inout",
    data: { label: `echo `, desc: `"4. TE query species: $4"` },
    position: { x: 160, y: 430 }
  },
  {
    id: "10",
    type: "inout",
    data: {
      label: `echo `,
      desc: `

########################################
### Step 1/5: Clustering with cd-hit 
########################################
`
    },
    position: { x: 160, y: 470 }
  },
  {
    id: "11",
    type: "process",
    data: { label: "cd-hit-est" },
    position: { x: 160, y: 510 }
  },
  {
    id: "12",
    type: "inout",
    data: {
      label: `echo `,
      desc: `

########################################
#### Step 2/5: Extracting cd-hit result
########################################
`
    },
    position: { x: 160, y: 550 }
  },
  {
    id: "13",
    type: "process",
    data: { label: "cat" },
    position: { x: 160, y: 590 }
  },
  {
    id: "14",
    type: "process",
    data: { label: "awk" },
    position: { x: 160, y: 630 }
  },
  {
    id: "15",
    type: "process",
    data: { label: "awk" },
    position: { x: 160, y: 670 }
  },
  {
    id: "16",
    type: "process",
    data: { label: "tr" },
    position: { x: 160, y: 710 }
  },
  {
    id: "17",
    type: "process",
    data: { label: "awk" },
    position: { x: 160, y: 750 }
  },
  {
    id: "18",
    type: "process",
    data: { label: "Rscript" },
    position: { x: 160, y: 810 }
  },
  {
    id: "19",
    type: "inout",
    data: {
      label: `echo `,
      desc: `

########################################
### Step 3/5: Running RepeatMasker 
########################################
`
    },
    position: { x: 160, y: 850 }
  },
  {
    id: "20",
    type: "cond",
    data: { label: "cond1" },
    position: { x: 160, y: 890 }
  },
  {
    id: "21",
    type: "inout",
    data: {
      label: `echo `,
      desc: `Custom TE database specified, ignored TE query species ***
	`
    },
    position: { x: 170, y: 910 }
  },
  {
    id: "22",
    type: "process",
    data: { label: "RepeatMasker" },
    position: { x: 170, y: 950 }
  },
  {
    id: "23",
    type: "inout",
    data: {
      label: `echo `,
      desc: `"No custom TE database specified, using the provided TE query species: $4 ***
	"`
    },
    position: { x: 150, y: 910 }
  },
  {
    id: "24",
    type: "process",
    data: { label: "RepeatMasker" },
    position: { x: 150, y: 950 }
  },
  { id: "25", type: "endif", position: { x: 170, y: 990 } },
  {
    id: "26",
    type: "inout",
    data: {
      label: `echo `,
      desc: `

########################################
###Step 4/5: Running RepeatProteinMask
########################################
`
    },
    position: { x: 170, y: 1010 }
  },
  {
    id: "27",
    type: "process",
    data: { label: "RepeatProteinMask" },
    position: { x: 170, y: 1050 }
  },
  {
    id: "28",
    type: "inout",
    data: {
      label: `echo `,
      desc: `

########################################
### Step 5/5: Calculating summary
########################################
`
    },
    position: { x: 170, y: 1090 }
  },
  {
    id: "29",
    type: "process",
    data: { label: "Rscript" },
    position: { x: 170, y: 1130 }
  },
  {
    id: "30",
    type: "inout",
    data: {
      label: `echo `,
      desc: `

########################################
### DONE
########################################`
    },
    position: { x: 170, y: 1170 }
  }
];
export default function App() {
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [elements, setElements] = useState(initialElements);
  const onConnect = (params) => setElements((els) => addEdge(params, els));
  const onElementsRemove = (elementsToRemove) =>
    setElements((els) => removeElements(elementsToRemove, els));
  const onLoad = (_reactFlowInstance) =>
    setReactFlowInstance(_reactFlowInstance);

  return (
    <div className="dndflow">
      <ReactFlowProvider>
        <div
          className="reactflow-wrapper"
          style={{ height: "500px", width: "500px" }}
          ref={reactFlowWrapper}
        >
          <ReactFlow
            elements={elements}
            onConnect={onConnect}
            onElementsRemove={onElementsRemove}
            nodeTypes={nodeTypes}
            onLoad={onLoad}
          >
            <Controls />
          </ReactFlow>
        </div>
      </ReactFlowProvider>
    </div>
  );
}
