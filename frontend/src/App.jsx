import { useState, useEffect } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import { fetchHealth, fetchUsers, triggerTask } from './services/api';

function App() {
  const [count, setCount] = useState(0);
  const [platformStatus, setPlatformStatus] = useState(null);
  const [taskResult, setTaskResult] = useState(null);
  const [users, setUsers] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchHealth()
      .then((data) => setPlatformStatus(data))
      .catch((err) => {
        // Fallback to legacy endpoint if needed
        fetch('http://localhost:8000/hello')
          .then((res) => res.json())
          .then((data) => setPlatformStatus({ service: data.message }))
          .catch((error) => console.error('Health check error:', error));
      });

    fetchUsers()
      .then((data) => setUsers(data))
      .catch((err) => {
        // Fallback to legacy endpoint if needed
        fetch('http://localhost:8000/users/')
          .then((res) => res.json())
          .then((data) => setUsers(data))
          .catch((error) => console.error('Fetch users error:', error));
      });
  }, []);

  const handleRunTask = () => {
    triggerTask()
      .then((data) => setTaskResult(data))
      .catch((err) => {
        // Fallback to legacy endpoint if needed
        fetch('http://localhost:8000/run-task')
          .then((res) => res.json())
          .then((data) => setTaskResult(data))
          .catch((error) => console.error('Error triggering task:', error));
      });
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem', fontFamily: 'sans-serif' }}>
      <header style={{ borderBottom: '1px solid #e0e0e0', paddingBottom: '1rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h1 style={{ margin: 0, color: '#1a73e8' }}>ALLINA Platform</h1>
            <p style={{ margin: '0.5rem 0 0', color: '#5f6368' }}>
              Multi-Tenant AI-Powered IT Operations Platform
            </p>
          </div>
          <div>
            <span style={{
              padding: '0.35rem 0.75rem',
              borderRadius: '12px',
              backgroundColor: platformStatus ? '#e6f4ea' : '#fce8e6',
              color: platformStatus ? '#137333' : '#c5221f',
              fontSize: '0.875rem',
              fontWeight: 500
            }}>
              {platformStatus ? `Status: ${platformStatus.status || 'Connected'}` : 'Connecting...'}
            </span>
          </div>
        </div>
      </header>

      {/* Navigation tabs */}
      <nav style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        {['overview', 'users', 'tasks'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '0.5rem 1rem',
              cursor: 'pointer',
              border: 'none',
              borderRadius: '4px',
              backgroundColor: activeTab === tab ? '#1a73e8' : '#f1f3f4',
              color: activeTab === tab ? '#ffffff' : '#3c4043',
              fontWeight: activeTab === tab ? 600 : 400
            }}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </nav>

      {/* Overview tab */}
      {activeTab === 'overview' && (
        <section style={{ backgroundColor: '#f8f9fa', padding: '1.5rem', borderRadius: '8px', marginBottom: '1.5rem' }}>
          <h3>7 Architectural Layers</h3>
          <ul style={{ lineHeight: '1.8' }}>
            <li><strong>L1 Entry Points:</strong> FastAPI v1 REST APIs & React Frontend</li>
            <li><strong>L2 Orchestrator:</strong> Central request coordinator & intent classification</li>
            <li><strong>L3 Specialist Agents:</strong> 12 AI agents (A1 Service Desk through A12 Employee Services)</li>
            <li><strong>L4 Shared Intelligence:</strong> RAG knowledge base, CMDB graph, and LLM gateway</li>
            <li><strong>L5 Trust & Governance:</strong> OPA policy engine, approval matrix, and tenant isolation</li>
            <li><strong>L6 Governed Automation:</strong> MCP tool gateway, Temporal workflows, Ansible/Terraform</li>
            <li><strong>L7 ELYSIUM Integrations:</strong> ITSM, Active Directory, Cloud, and Infrastructure</li>
          </ul>
          <div style={{ marginTop: '1rem' }}>
            <button onClick={() => setCount((c) => c + 1)} style={{ padding: '0.5rem 1rem' }}>
              Interactive Counter: {count}
            </button>
          </div>
        </section>
      )}

      {/* Users tab */}
      {activeTab === 'users' && (
        <section style={{ backgroundColor: '#ffffff', border: '1px solid #dadce0', padding: '1.5rem', borderRadius: '8px' }}>
          <h3>Users (Database Access)</h3>
          {users.length > 0 ? (
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #e0e0e0', textAlign: 'left' }}>
                  <th style={{ padding: '0.5rem' }}>ID</th>
                  <th style={{ padding: '0.5rem' }}>Name</th>
                  <th style={{ padding: '0.5rem' }}>Email</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id} style={{ borderBottom: '1px solid #f1f3f4' }}>
                    <td style={{ padding: '0.5rem' }}>{u.id}</td>
                    <td style={{ padding: '0.5rem' }}>{u.name || u.full_name}</td>
                    <td style={{ padding: '0.5rem' }}>{u.email}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p style={{ color: '#5f6368' }}>No users retrieved. Ensure backend database is running and migrated.</p>
          )}
        </section>
      )}

      {/* Tasks tab */}
      {activeTab === 'tasks' && (
        <section style={{ backgroundColor: '#ffffff', border: '1px solid #dadce0', padding: '1.5rem', borderRadius: '8px' }}>
          <h3>Celery Background Task Execution</h3>
          <p>Dispatches asynchronous background jobs to Celery worker via Redis.</p>
          <button
            onClick={handleRunTask}
            style={{ padding: '0.6rem 1.2rem', backgroundColor: '#1a73e8', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Trigger Background Task
          </button>
          {taskResult && (
            <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#e8f0fe', borderRadius: '4px' }}>
              <p><strong>Status:</strong> {taskResult.status}</p>
              {taskResult.task_id && <p><strong>Task ID:</strong> {taskResult.task_id}</p>}
              {taskResult.result !== undefined && taskResult.result !== null && (
                <p><strong>Result:</strong> {taskResult.result}</p>
              )}
            </div>
          )}
        </section>
      )}
    </div>
  );
}

export default App;
