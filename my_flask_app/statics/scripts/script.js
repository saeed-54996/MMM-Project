document.addEventListener('DOMContentLoaded', () => {
    // For writer-photographer table
    const addRowButtonWriter = document.getElementById('add-row');
    const tableBodyWriter = document.querySelector('#info-table tbody');

    if (addRowButtonWriter) {
        handleTableActions(addRowButtonWriter, tableBodyWriter);
    }

    // For article table
    const addRowButtonArticle = document.getElementById('add-row-article');
    const tableBodyArticle = document.querySelector('#article-table tbody');

    if (addRowButtonArticle) {
        handleTableActions(addRowButtonArticle, tableBodyArticle);
    }

    function handleTableActions(addRowButton, tableBody) {
        addRowButton.addEventListener('click', () => {
            const lastRow = tableBody.querySelector('tr:last-child');
            const inputs = lastRow.querySelectorAll('input');

            let allFilled = true;
            inputs.forEach(input => {
                if (!input.value) {
                    allFilled = false;
                }
            });

            if (allFilled) {
                const newRow = document.createElement('tr');
                inputs.forEach(input => {
                    const cell = document.createElement('td');
                    if (input.name === 'name' || input.name === 'title') {
                        const link = document.createElement('a');
                        link.href = '#';
                        link.textContent = input.value;
                        cell.appendChild(link);
                    } else {
                        cell.textContent = input.value;
                    }
                    newRow.appendChild(cell);
                });

                const actionCell = document.createElement('td');
                const editButton = document.createElement('button');
                editButton.textContent = 'ویرایش';
                editButton.className = 'edit-button';
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'حذف';
                deleteButton.className = 'delete-button';
                actionCell.appendChild(editButton);
                actionCell.appendChild(deleteButton);
                newRow.appendChild(actionCell);

                tableBody.insertBefore(newRow, lastRow);

                inputs.forEach(input => {
                    input.value = '';
                });
            } else {
                alert('لطفاً تمامی فیلدها را پر کنید.');
            }
        });

        tableBody.addEventListener('click', (event) => {
            const target = event.target;
            if (target.classList.contains('edit-button')) {
                handleEditRow(target);
            } else if (target.classList.contains('delete-button')) {
                handleDeleteRow(target);
            }
        });

        function handleEditRow(button) {
            const row = button.closest('tr');
            const cells = row.querySelectorAll('td:not(:last-child)');
            cells.forEach(cell => {
                if (cell.querySelector('a')) {
                    const link = cell.querySelector('a');
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = link.textContent;
                    cell.textContent = '';
                    cell.appendChild(input);
                } else {
                    const text = cell.textContent.trim();
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = text;
                    cell.textContent = '';
                    cell.appendChild(input);
                }
            });

            const editButton = row.querySelector('.edit-button');
            editButton.textContent = 'ذخیره';
            editButton.classList.remove('edit-button');
            editButton.classList.add('save-button');

            editButton.addEventListener('click', handleSaveRow);
        }
        function handleSaveRow(event) {
            const button = event.target;
            const row = button.closest('tr');
            const cells = row.querySelectorAll('td:not(:last-child)');
            cells.forEach(cell => {
                const input = cell.querySelector('input');
                if (cell.querySelector('a')) {
                    const link = document.createElement('a');
                    link.href = '#';
                    link.textContent = input.value;
                    cell.textContent = '';
                    cell.appendChild(link);
                } else {
                    cell.textContent = input.value;
                }
            });

            button.textContent = 'ویرایش';
            button.classList.remove('save-button');
            button.classList.add('edit-button');
        }

        function handleDeleteRow(button) {
            const row = button.closest('tr');
            row.remove();
        }
    }

    // For picture gallery
    const gallery = document.getElementById('gallery');
    const addPictureButton = document.getElementById('add-picture');

    if (gallery && addPictureButton) {
        // Example pictures array
        const pictures = [
            { src: 'path/to/image1.jpg', title: 'Title 1', description: 'Description 1' },
            { src: 'path/to/image2.jpg', title: 'Title 2', description: 'Description 2' },
            { src: 'path/to/image3.jpg', title: 'Title 3', description: 'Description 3' },
            { src: 'path/to/image4.jpg', title: 'Title 4', description: 'Description 4' }
        ];

        function addPictures(pictureArray) {
            pictureArray.forEach(picture => {
                const pictureItem = document.createElement('div');
                pictureItem.classList.add('picture-item');

                const img = document.createElement('img');
                img.src = picture.src;
                img.alt = picture.title;

                const title = document.createElement('div');
                title.classList.add('title');
                title.textContent = picture.title;

                const description = document.createElement('div');
                description.classList.add('description');
                description.textContent = picture.description;

                pictureItem.appendChild(img);
                pictureItem.appendChild(title);
                pictureItem.appendChild(description);

                gallery.appendChild(pictureItem);
            });
        }

        // Add initial pictures
        addPictures(pictures);

        addPictureButton.addEventListener('click', () => {
            const src = prompt('Enter image URL:');
            const title = prompt('Enter image title:');
            const description = prompt('Enter image description:');
            if (src && title && description) {
                addPictures([{ src, title, description }]);
            } else {
                alert('Please fill all fields.');
            }
        });
    }
});