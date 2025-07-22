import React from 'react';

const PipelineDisplay = ({ pipeline }) => {
  if (!pipeline || pipeline.length === 0) return null;

  return (
    <div className="pipeline-display">
      <h2>Pipeline Execution:</h2>
      <ul>
        {pipeline.map((step, index) => (
          <li key={index}>
            <strong>{step.name}</strong>: {step.output}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PipelineDisplay;
