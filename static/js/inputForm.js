
function alerted() {
    let x = document.getElementById("file");
    let txt = "";
  
    if ('files' in x && (x.files.length != 0)) 
    {
      var file = x.files[0];
      if ('name' in file) {
        txt += "name: " + file.name;
      }
      if ('size' in file) {
        txt += " size: " + file.size + " bytes";
      }
    } 
    else
    {
      txt = "Select one or more files.";
    }
  
    alert(txt);
  }
  
  
  function dropHandler(ev) {
    console.log('File(s) dropped');
  
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
  
    if (ev.dataTransfer.items) {
      // Use DataTransferItemList interface to access the file(s)
      for (var i = 0; i < ev.dataTransfer.items.length; i++) {
        // If dropped items aren't files, reject them
        if (ev.dataTransfer.items[i].kind === 'file') {
          var file = ev.dataTransfer.items[i].getAsFile();
          alert('... file[' + i + '].name = ' + file.name);
        }
      }
    } else {
      // Use DataTransfer interface to access the file(s)
      for (var i = 0; i < ev.dataTransfer.files.length; i++) {
        alert('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
      }
    }
  }
  
  function dragOverHandler(ev) {
    console.log('File(s) in drop zone');
  
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
  }