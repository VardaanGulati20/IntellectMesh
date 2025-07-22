import React from 'react';
import { useState } from 'react';

import '../App.css';
import Header from './header';
import QueryForm from './QueryForm';
import AnswerDisplay from './AnswerDisplay';
import PipelineView from './PipelineView';

function App() {
  const [answer, setAnswer] = useState('');
  const [pipeline, setPipeline] = useState([]);

  const handleResponse = (data) => {
    setAnswer(data.answer || '');
    setPipeline(data.pipeline || []);
  };

  return (
    <div className="main-container">
      <Header />
      <QueryForm onResponse={handleResponse} />
      {answer && <AnswerDisplay answer={answer} />}
      {pipeline.length > 0 && <PipelineView pipeline={pipeline} />}
    </div>
  );
}

export default App;
