import React, { useState, useEffect } from 'react';
import './UploadDetailPopUp.css';

export interface UploadFormData {
  title: string;
  authors: Array<{ name: string; surname: string }>;
  publisher: string;
  year: string;
  topic: string;
}

interface UploadDetailPopUpProps {
  fileName: string;
  onSubmit: (data: UploadFormData) => void;
  onCancel: () => void;
}

export const UploadDetailPopUp: React.FC<UploadDetailPopUpProps> = ({ fileName, onSubmit, onCancel }) => {
  const [title, setTitle] = useState(fileName.replace(/\.pdf$/i, ''));
  const [authors, setAuthors] = useState<{ name: string; surname: string }[]>([{ name: '', surname: '' }]);
  const [publisher, setPublisher] = useState('');
  const [year, setYear] = useState('');
  const [topic, setTopic] = useState('');
  const [topicError, setTopicError] = useState(false);

  const handleAuthorChange = (index: number, field: 'name' | 'surname', value: string) => {
    const newAuthors = [...authors];
    newAuthors[index][field] = value;
    setAuthors(newAuthors);
  };

  const addAuthor = () => {
    setAuthors([...authors, { name: '', surname: '' }]);
  };

  const removeAuthor = (index: number) => {
    const newAuthors = authors.filter((_, i) => i !== index);
    setAuthors(newAuthors);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) {
      setTopicError(true);
      return;
    }
    setTopicError(false);
    onSubmit({
      title,
      authors: authors.filter(a => a.name.trim() || a.surname.trim()),
      publisher,
      year,
      topic,
    });
  };

  // Close modal on Escape key press
  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onCancel();
      }
    };
    window.addEventListener('keydown', handleEsc);
    return () => {
      window.removeEventListener('keydown', handleEsc);
    };
  }, [onCancel]);

  return (
    <div className="udp-overlay" onClick={(e) => { if (e.target === e.currentTarget) onCancel(); }}>
      <div className="udp-modal">
        <h2 className="udp-title">Upload a text</h2>
        <div className="udp-subtitle">Enter the information about the book you're uploading</div>
        <form className="udp-form" onSubmit={handleSubmit} autoComplete="off">
          <label className="udp-label">
            TITLE
            <input
              className="udp-input udp-title-input"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </label>

          <div className="udp-authors-section">
            {authors.map((author, index) => (
              <div key={index} className="udp-author-row">
                <input
                  className="udp-input udp-author-input"
                  type="text"
                  placeholder="Enter author name"
                  value={author.name}
                  onChange={(e) => handleAuthorChange(index, 'name', e.target.value)}
                />
                <input
                  className="udp-input udp-author-input"
                  type="text"
                  placeholder="Enter author surname"
                  value={author.surname}
                  onChange={(e) => handleAuthorChange(index, 'surname', e.target.value)}
                />
                {authors.length > 1 && (
                  <button
                    type="button"
                    className="udp-remove-author-btn"
                    onClick={() => removeAuthor(index)}
                  >
                    🗑️
                  </button>
                )}
              </div>
            ))}
            <button type="button" className="udp-add-author-btn" onClick={addAuthor}>
              + Add author
            </button>
          </div>

          <div className="udp-pubyear-row">
            <input
              className="udp-input udp-publisher-input"
              type="text"
              placeholder="Enter publisher"
              value={publisher}
              onChange={(e) => setPublisher(e.target.value)}
            />
            <input
              className="udp-input udp-year-input"
              type="text"
              placeholder="Enter year"
              maxLength={4}
              pattern="\d{4}"
              value={year}
              onChange={(e) => setYear(e.target.value)}
            />
          </div>

          <input
            className={`udp-input udp-topic-input ${topicError ? 'udp-input-error' : ''}`}
            type="text"
            placeholder="Enter topic"
            value={topic}
            onChange={(e) => {
              setTopic(e.target.value);
              if (e.target.value.trim()) setTopicError(false);
            }}
            required
          />
          {topicError && <p className="udp-error-message">Topic is required.</p>}


          <div className="udp-btn-row">
            <button type="button" className="udp-cancel-btn" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="udp-upload-btn">
              Upload
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}; 