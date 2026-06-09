import './App.css'

function App() {

  return (
    <div>
      const downloadImage = (base64Data: string, fileName: string) => {
  // Create a temporary link element
  const link = document.createElement("a");
  link.href = base64Data; // This is your "data:image/jpeg;base64,..." string
  link.download = fileName; // The name the file will have when saved
  
  // Append to body, click it, and remove it
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
    </div>
  )
}

export default App
