import React from 'react';
import { Map, ArrowLeft, BrainCircuit } from 'lucide-react';
import AdaptiveRoadmap from '../components/AdaptiveRoadmap';

export default function RoadmapPage({ onSelectProblem, onNavigate }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Top Navigation Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
        <button
          type="button"
          className="btn btn-secondary btn-sm"
          onClick={() => onNavigate && onNavigate('dashboard')}
          style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}
        >
          <ArrowLeft size={14} /> Back to Dashboard
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span className="badge badge-purple" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <BrainCircuit size={12} /> Adaptive Curriculum
          </span>
          <span className="badge badge-blue">
            Prerequisite-Aware Knowledge Graph
          </span>
        </div>
      </div>

      {/* Main Roadmap Component */}
      <AdaptiveRoadmap onSelectProblem={onSelectProblem} onNavigate={onNavigate} />
    </div>
  );
}
