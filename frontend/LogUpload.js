import React, { useState } from 'react';

const LogFileUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadStatus('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault(); 

    if (!selectedFile) {
      setUploadStatus('Please select a file to upload.');
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
        setUploadStatus('File uploaded successfully!');
      } else {
        setUploadStatus('Failed to upload file.');
      }
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
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