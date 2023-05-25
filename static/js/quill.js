let quill;
document.addEventListener('DOMContentLoaded', function () {
  quill = new Quill('#generated-text', {
    theme: 'snow',
    modules: {
      toolbar: [
        ['save'],
        [{ 'header': 1 }, { 'header': 2 }],
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
        [{ 'indent': '-1' }, { 'indent': '+1' }],
        [{ 'direction': 'rtl' }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'font': [] }],
        [{ 'align': [] }],
        [{ 'script': 'sub' }, { 'script': 'super' }],
        ['blockquote', 'code-block'],
        ['clean'],
      ],
      history: {
        delay: 1000,
        maxStack: 50,
        userOnly: true
      },
    },
  });
  async function saveContent() {
    const content = quill.root.innerHTML;
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = content;
    const maxWidth = 500;
    const { PDFDocument,StandardFonts, rgb } = PDFLib;
    const pdfDoc = await PDFDocument.create();
    const timesRomanFont = await pdfDoc.embedFont(StandardFonts.Helvetica);
    let cursor = {
      x:50,
      y:750
    }
    let page = pdfDoc.addPage([600, 800]);
    tempDiv.querySelectorAll('p, h1, h2, h3, h4, h5, h6, blockquote').forEach((element,line) => {
      const textSize = parseFloat(window.getComputedStyle(element).fontSize || 16);
      const text = element.textContent;
      cursor.x = 50
      cursor.y = line  ? cursor.y-(textSize + 10)*1 : cursor.y
      text.split(' ').forEach((word,index,array)=>{
        const spaceWidth = timesRomanFont.widthOfTextAtSize(array[index-1] || '', textSize);
        const wordWidth = timesRomanFont.widthOfTextAtSize(word, textSize);

        if (wordWidth+cursor.x>maxWidth){
          cursor.x = 50;
          cursor.y -= textSize + 10;
        }
        else {
          cursor.x += spaceWidth+2
        }
        if (cursor.y <= 50){
          page = pdfDoc.addPage([600, 800]);
          cursor.y = 750;
        }
        page.drawText(word, {
          x: cursor.x,
          y: cursor.y,
          size: textSize,
          font: timesRomanFont,
          color: rgb(0, 0, 0),
        });
      })
    });

    const pdfBytes = await pdfDoc.save();
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'generated-text.pdf';
    link.click();
  }

  const toolbar = quill.getModule('toolbar');

  const saveBtn = document.querySelector('.ql-save');
  saveBtn.classList.add('ql-save');
  saveBtn.innerHTML = '📝';
  saveBtn.addEventListener('click', saveContent);
  toolbar.container.appendChild(saveBtn);

  const redoBtn = document.createElement('button');
  redoBtn.classList.add('ql-redo');
  redoBtn.innerHTML = '↷';
  redoBtn.addEventListener('click', () => {
    quill.history.redo();
  });
  toolbar.container.appendChild(redoBtn);

  
  const undoBtn = document.createElement('button');
  undoBtn.classList.add('ql-undo');
  undoBtn.innerHTML = '↶';
  undoBtn.addEventListener('click', () => {
    quill.history.undo();
  });
  toolbar.container.appendChild(undoBtn);
  
});

// export { quill };