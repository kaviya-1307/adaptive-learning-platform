import React, { useRef } from 'react';
import Editor, { loader } from '@monaco-editor/react';
import * as monaco from 'monaco-editor';
import { RotateCcw, Copy, Check, Code2 } from 'lucide-react';

// Configure Monaco to load from locally installed npm package instead of CDN
loader.config({ monaco });

export default function CodeEditor({
  code,
  value,
  onChange,
  onReset,
  disabled = false,
  language = 'python',
  supportedLanguages = ['python'],
  onLanguageChange,
}) {
  const [copied, setCopied] = React.useState(false);
  const editorRef = useRef(null);
  const displayCode = code !== undefined ? code : (value !== undefined ? value : '');

  const languageLabels = {
    python: 'Python 3',
    java: 'Java 21',
    cpp: 'C++ 17',
    javascript: 'JavaScript (Node)',
  };

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
  };

  const handleCopy = () => {
    if (displayCode) {
      navigator.clipboard.writeText(displayCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const monacoLanguage = language === 'javascript' ? 'javascript' : (language === 'cpp' ? 'cpp' : (language === 'java' ? 'java' : 'python'));

  return (
    <div className="code-editor-container" style={{ display: 'flex', flexDirection: 'column', height: '100%', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-md)', overflow: 'hidden', background: '#1e1e1e' }}>
      {/* Editor Header / Toolbar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0.5rem 0.875rem',
          background: '#252526',
          borderBottom: '1px solid #333333',
          fontSize: '0.8125rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', color: '#cccccc', fontWeight: 500 }}>
          <Code2 size={16} color="#38bdf8" />
          {/* Language Selector */}
          <select
            value={language}
            onChange={(e) => onLanguageChange && onLanguageChange(e.target.value)}
            disabled={disabled}
            style={{
              background: '#18181b',
              color: '#38bdf8',
              border: '1px solid #3f3f46',
              borderRadius: 'var(--radius-sm, 4px)',
              padding: '0.2rem 0.5rem',
              fontSize: '0.8125rem',
              fontWeight: 600,
              cursor: 'pointer',
              outline: 'none',
            }}
          >
            {supportedLanguages.map((lang) => (
              <option key={lang} value={lang}>
                {languageLabels[lang] || lang}
              </option>
            ))}
          </select>
          <span style={{ color: '#666', margin: '0 0.25rem' }}>|</span>
          <span style={{ color: '#888', fontSize: '0.75rem' }}>Solution Runner</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleCopy}
            title="Copy code to clipboard"
            style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', height: '26px' }}
          >
            {copied ? <Check size={13} color="#4ade80" /> : <Copy size={13} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={onReset}
            disabled={disabled}
            title="Reset to starter template"
            style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', height: '26px' }}
          >
            <RotateCcw size={13} />
            <span>Reset</span>
          </button>
        </div>
      </div>

      {/* Monaco Editor Mount */}
      <div style={{ flex: 1, minHeight: '320px', position: 'relative' }}>
        <Editor
          key={`monaco-${monacoLanguage}`}
          height="100%"
          defaultLanguage={monacoLanguage}
          language={monacoLanguage}
          theme="vs-dark"
          value={displayCode}
          onChange={onChange}
          onMount={handleEditorDidMount}
          options={{
            fontSize: 14,
            fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace",
            minimap: { enabled: false },
            lineNumbers: 'on',
            roundedSelection: true,
            scrollBeyondLastLine: false,
            readOnly: disabled,
            automaticLayout: true,
            tabSize: 4,
            insertSpaces: true,
            wordWrap: 'on',
            cursorBlinking: 'smooth',
            smoothScrolling: true,
            contextmenu: true,
            renderLineHighlight: 'all',
          }}
          loading={
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#888' }}>
              Loading Monaco {languageLabels[language] || language} Editor...
            </div>
          }
        />
      </div>
    </div>
  );
}
