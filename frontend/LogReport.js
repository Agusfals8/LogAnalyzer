import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT;

const LogAnalysisReport = () => {
  const [logData, setLogData] = useState({
    keyMetrics: {},
    identifiedAnomalies: [],
    otherRelevantData: {},
  });

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLogData = async () => {
    try {
      const response = await axios.get(`${API_ENDPOINT}/log-data`);
      setLogData(response.data);
      setIsLoading(false);
    } catch (error) {
      setError(error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLogData();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div>
      <h1>Log Analysis Report</h1>
      <section>
        <h2>Key Metrics</h2>
        <ul>
          {Object.entries(logData.keyMetrics).map(([key, value]) => (
            <li key={key}>{`${key}: ${value}`}</li>
          ))}
        </ul>
      </section>
      <section>
        <h2>Identified Anomalies</h2>
        <ul>
          {logData.identifiedAnomalies.map((anomaly, index) => (
            <li key={index}>{anomaly}</li>
          ))}
        </ul>
      </section>
      <section>
        <h2>Other Relevant Data</h2>
        <ul>
          {Object.entries(logData.otherRelevantData).map(([key, value]) => (
            <li key={key}>{`${key}: ${value}`}</li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default LogAnalysisReport;