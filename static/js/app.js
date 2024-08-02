let deferredPrompt;
const addBtn = document.createElement('button');
addBtn.style.display = 'none';
addBtn.textContent = 'Add to Home Screen';

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    addBtn.style.display = 'block';

    addBtn.addEventListener('click', (e) => {
        addBtn.style.display = 'none';
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the A2HS prompt');
            } else {
                console.log('User dismissed the A2HS prompt');
            }
            deferredPrompt = null;
        });
    });
});

// Dynamic table of contents generation for viewer page
if (document.querySelector('.markdown-content')) {
    const content = document.querySelector('.markdown-content');
    const headings = content.querySelectorAll('h1, h2, h3, h4, h5, h6');
    
    if (headings.length > 0) {
        const toc = document.createElement('nav');
        toc.className = 'table-of-contents';
        const tocTitle = document.createElement('h2');
        tocTitle.textContent = '目次';
        toc.appendChild(tocTitle);
        const tocList = document.createElement('ul');

        headings.forEach((heading, index) => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            const headingId = `heading-${index}`;
            heading.id = headingId;
            a.href = `#${headingId}`;
            a.textContent = heading.textContent;
            a.className = `toc-${heading.tagName.toLowerCase()}`;
            li.appendChild(a);
            tocList.appendChild(li);
        });

        toc.appendChild(tocList);
        content.insertBefore(toc, content.firstChild);
    }
}