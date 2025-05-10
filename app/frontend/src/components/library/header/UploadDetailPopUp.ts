import './UploadDetailPopUp.css';

export function UploadDetailPopUp({
  fileName,
  onSubmit,
  onCancel
}: {
  fileName: string,
  onSubmit: (data: any) => void,
  onCancel: () => void
}) {
  // Modal overlay
  const overlay = document.createElement('div');
  overlay.className = 'udp-overlay';

  // Modal container
  const modal = document.createElement('div');
  modal.className = 'udp-modal';

  // Title
  const title = document.createElement('h2');
  title.className = 'udp-title';
  title.textContent = 'Upload a text';

  // Subtitle
  const subtitle = document.createElement('div');
  subtitle.className = 'udp-subtitle';
  subtitle.textContent = "Enter the information about the book you're uploading";

  // Form
  const form = document.createElement('form');
  form.className = 'udp-form';
  form.autocomplete = 'off';

  // Title field
  const titleLabel = document.createElement('label');
  titleLabel.className = 'udp-label';
  titleLabel.textContent = 'TITLE';
  const titleInput = document.createElement('input');
  titleInput.className = 'udp-input udp-title-input';
  titleInput.type = 'text';
  titleInput.value = fileName.replace(/\.pdf$/i, '');
  titleInput.required = true;
  titleLabel.appendChild(titleInput);

  // Authors section
  const authorsContainer = document.createElement('div');
  authorsContainer.className = 'udp-authors-container';
  let authors = [{ name: '', surname: '' }];

  function renderAuthors() {
    authorsContainer.innerHTML = '';
    authors.forEach((author, idx) => {
      const row = document.createElement('div');
      row.className = 'udp-author-row';

      // Author name
      const nameInput = document.createElement('input');
      nameInput.className = 'udp-input udp-author-input';
      nameInput.type = 'text';
      nameInput.placeholder = 'Enter author name';
      nameInput.value = author.name;
      nameInput.oninput = (e) => {
        authors[idx].name = nameInput.value;
      };
      row.appendChild(nameInput);

      // Author surname
      const surnameInput = document.createElement('input');
      surnameInput.className = 'udp-input udp-author-input';
      surnameInput.type = 'text';
      surnameInput.placeholder = 'Enter author surname';
      surnameInput.value = author.surname;
      surnameInput.oninput = (e) => {
        authors[idx].surname = surnameInput.value;
      };
      row.appendChild(surnameInput);

      // Remove button (only if more than one author)
      if (authors.length > 1) {
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'udp-remove-author-btn';
        removeBtn.innerHTML = '🗑️';
        removeBtn.onclick = () => {
          authors.splice(idx, 1);
          renderAuthors();
        };
        row.appendChild(removeBtn);
      }

      authorsContainer.appendChild(row);
    });
  }
  renderAuthors();

  // Add author button
  const addAuthorBtn = document.createElement('button');
  addAuthorBtn.type = 'button';
  addAuthorBtn.className = 'udp-add-author-btn';
  addAuthorBtn.textContent = '+ Add author';
  addAuthorBtn.onclick = () => {
    authors.push({ name: '', surname: '' });
    renderAuthors();
  };

  // Publisher and year
  const pubYearRow = document.createElement('div');
  pubYearRow.className = 'udp-pubyear-row';

  const publisherInput = document.createElement('input');
  publisherInput.className = 'udp-input udp-publisher-input';
  publisherInput.type = 'text';
  publisherInput.placeholder = 'Enter publisher';

  const yearInput = document.createElement('input');
  yearInput.className = 'udp-input udp-year-input';
  yearInput.type = 'text';
  yearInput.placeholder = 'Enter year';
  yearInput.maxLength = 4;
  yearInput.pattern = '\\d{4}';

  pubYearRow.appendChild(publisherInput);
  pubYearRow.appendChild(yearInput);

  // Topic
  const topicInput = document.createElement('input');
  topicInput.className = 'udp-input udp-topic-input';
  topicInput.type = 'text';
  topicInput.placeholder = 'Enter topic';
  topicInput.required = true;

  // Buttons row
  const btnRow = document.createElement('div');
  btnRow.className = 'udp-btn-row';

  const cancelBtn = document.createElement('button');
  cancelBtn.type = 'button';
  cancelBtn.className = 'udp-cancel-btn';
  cancelBtn.textContent = 'Cancel';
  cancelBtn.onclick = (e) => {
    e.preventDefault();
    onCancel();
    overlay.remove();
  };

  const uploadBtn = document.createElement('button');
  uploadBtn.type = 'submit';
  uploadBtn.className = 'udp-upload-btn';
  uploadBtn.textContent = 'Upload';

  btnRow.appendChild(cancelBtn);
  btnRow.appendChild(uploadBtn);

  // Form submit
  form.onsubmit = (e) => {
    e.preventDefault();
    if (!topicInput.value.trim()) {
      topicInput.classList.add('udp-input-error');
      topicInput.focus();
      return;
    }
    topicInput.classList.remove('udp-input-error');
    onSubmit({
      title: titleInput.value,
      authors: authors.filter(a => a.name || a.surname),
      publisher: publisherInput.value,
      year: yearInput.value,
      topic: topicInput.value
    });
    overlay.remove();
  };

  // Assemble form
  form.appendChild(titleLabel);
  form.appendChild(authorsContainer);
  form.appendChild(addAuthorBtn);
  form.appendChild(pubYearRow);
  form.appendChild(topicInput);
  form.appendChild(btnRow);

  // Assemble modal
  modal.appendChild(title);
  modal.appendChild(subtitle);
  modal.appendChild(form);
  overlay.appendChild(modal);

  // Close on overlay click (optional, can be removed for stricter UX)
  overlay.onclick = (e) => {
    if (e.target === overlay) {
      onCancel();
      overlay.remove();
    }
  };

  return overlay;
}
