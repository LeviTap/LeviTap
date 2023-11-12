document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('runPythonCode').addEventListener('click', function () {
    fetch('http://localhost:5000/run-python-code', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        document.getElementById('output').innerText = data.message;
      })
      .catch(error => console.error('Error:', error));
  });
});
