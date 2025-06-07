const cropEmojis = {
  'TOMATO': '🍅',
  'GARLIC': '🧄',
  'ONION': '🧅',
  'ORANGE': '🍊',
  'PEAS': '🟢',
  'POTATO': '🥔',
  'RICE': '🌾',
  'SUGARCANE': '🎋'
};

document.getElementById('cropForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  // Show loading state
  document.getElementById('emptyState').style.display = 'none';
  document.getElementById('recommendations').style.display = 'none';
  document.getElementById('loadingState').style.display = 'flex';
  
  try {
      const formData = new FormData(this);
      const data = Object.fromEntries(formData);
      
      console.log(data)
      // Call the Flask API
      const response = await fetch('/users/analyse', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              nitrogen: parseFloat(data.nitrogen),
              phosphorous: parseFloat(data.phosphorous),
              potassium: parseFloat(data.potassium),
              temperature: parseFloat(data.temperature),  
              pH: parseFloat(data.ph),
          })
      });
      
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const htmlContent = await response.text();
      document.open()
      document.write(htmlContent);
      document.close();
      
      
      /* document.getElementById('loadingState').style.display = 'none';
      document.getElementById('recommendations').style.display = 'block'; */
      
  } catch (error) {
      console.error('Error calling API:', error);
      
      // Show error message to user
      document.getElementById('loadingState').style.display = 'none';
      showErrorMessage('Failed to get crop recommendations. Please try again.');
  }
});

/* function displayRecommendations(predictions) { 
  const resultsDiv = document.getElementById('cropResults');
  
  // Handle different response formats from your API
  let primary, secondary, tertiary;
  
  if (predictions.primary && predictions.secondary && predictions.tertiary) {
      // If API returns object with primary/secondary/tertiary
      primary = predictions.primary;
      secondary = predictions.secondary;
      tertiary = predictions.tertiary;
  } else if (Array.isArray(predictions) && predictions.length >= 3) {
      // If API returns array of predictions
      primary = predictions[0];
      secondary = predictions[1];
      tertiary = predictions[2];
  } else if (typeof predictions === 'string') {
      // If API returns single prediction
      primary = predictions;
      secondary = 'POTATO'; // fallback
      tertiary = 'ONION';   // fallback
  } else {
      // Handle unexpected response format
      console.error('Unexpected API response format:', predictions);
      
  }
  
  resultsDiv.innerHTML = `
      <div class="crop-card primary" style="animation-delay: 0.1s">
          <div class="crop-icon">${cropEmojis[primary] || '🌱'}</div>
          <h3>Best Match: ${primary}</h3>
          <p>Highest compatibility with your soil conditions</p>
      </div>
      <div class="crop-card secondary" style="animation-delay: 0.3s">
          <div class="crop-icon">${cropEmojis[secondary] || '🌱'}</div>
          <h4>Alternative: ${secondary}</h4>
          <p>Good secondary option for diversification</p>
      </div>
      <div class="crop-card tertiary" style="animation-delay: 0.5s">
          <div class="crop-icon">${cropEmojis[tertiary] || '🌱'}</div>
          <h4>Third Choice: ${tertiary}</h4>
          <p>Consider for crop rotation</p>
      </div>
  `;
}*/

function showErrorMessage(message) {
  const resultsDiv = document.getElementById('cropResults');
  resultsDiv.innerHTML = `
      <div class="error-message" style="
          background-color: #fee2e2;
          border: 1px solid #fecaca;
          color: #dc2626;
          padding: 1rem;
          border-radius: 8px;
          text-align: center;
          margin: 1rem 0;
      ">
          <h4>⚠️ Error</h4>
          <p>${message}</p>
          <button onclick="location.reload()" style="
              background-color: #dc2626;
              color: white;
              border: none;
              padding: 0.5rem 1rem;
              border-radius: 4px;
              cursor: pointer;
              margin-top: 0.5rem;
          ">Try Again</button>
      </div>
  `;
  
  document.getElementById('recommendations').style.display = 'block';
}
