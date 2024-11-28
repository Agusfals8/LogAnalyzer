import React, { useState } from 'react';

const LogFileUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadStatus('');
  };

  const logToConsole = (message) => {
    console.log(message);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      const message = 'Please select a file to upload.';
      setUploadStatus(message);
      logToConsole(message);
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(process.env.REACT_APP_UPLOAD_URL, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const successMessage = 'File uploaded successfully!';
        setUploadStatus(successMessage);
        logToConsole(successMessage);
      } else {
        const failureMessage = 'Failed to upload file.';
        setUploadStatus(failureMessage);
        logToConsole(failureMessage);
      }
    } catch (error) {
      const errorMessage = `Error: ${error.message}`;
      setUploadStatus(errorMessage);
      logToConsole(errorMessage);
    }
  };

  return (
    <div>
      <h3>Upload Log File</h3>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
};

export default LogFileUploader;